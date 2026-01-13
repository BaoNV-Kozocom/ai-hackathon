<?php

namespace App\Http\Controllers\Api;

use App\Events\MessageCreated;
use App\Http\Controllers\Controller;
use App\Jobs\AnalyzeLogJob;
use App\Models\IssueThread;
use App\Models\Project;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class IngestLogController extends Controller
{
    public function store(Request $request)
    {
        // 1. Auth & Validation
        $apiKey = $request->header('X-API-Key');
        if (!$apiKey) {
            return response()->json(['error' => 'Missing X-API-Key header'], 401);
        }

        $project = Project::where('api_key', $apiKey)->first();
        if (!$project) {
            return response()->json(['error' => 'Invalid API Key'], 401);
        }

        $payload = $request->validate([
            'message' => 'required|string',
            'level' => 'required|string', // e.g., 'error', 'critical'
            'trace' => 'nullable|string',
            'environment' => 'required|string',
        ]);

        // 2. Hash the error to find existing thread or create new
        // Normalized hash: message + trace
        $errorHash = md5($payload['message'] . ($payload['trace'] ?? ''));

        $thread = IssueThread::firstOrCreate(
            [
                'project_id' => $project->id,
                'error_hash' => $errorHash
            ],
            [
                'title' => Str::limit($payload['message'], 100),
                'status' => 'open',
                'severity' => $this->mapSeverity($payload['level']),
                'environment' => $payload['environment'],
                'source_service' => $request->input('service', 'unknown'), // Optional service name
            ]
        );

        // If thread was resolved but same error occurs, maybe reopen it? 
        // For now, let's keep it simple.

        // 3. Create the System Log Message
        $message = $thread->messages()->create([
            'sender_type' => 'system_log',
            'content' => $payload['message'] . "\n\n" . ($payload['trace'] ?? ''),
            'meta_data' => ['raw_payload' => $payload],
        ]);

        // 4. Update Thread Activity
        $thread->touch('latest_activity_at');

        // 5. Broadcast to Real-time Channel
        MessageCreated::dispatch($message);

        // 6. Trigger AI Analysis (Async)
        // Only if it's the first execution or if we want to re-analyze every occurrence? 
        // Usually only analyze if there isn't a recent analysis. 
        // For this MVP, we analyze every time a new log thread is created OR maybe just always for demo.
        // Let's analyze if the thread has < 2 messages (fresh) or if status is open.
        AnalyzeLogJob::dispatch($message);

        return response()->json([
            'success' => true,
            'thread_id' => $thread->id,
            'message_id' => $message->id
        ], 201);
    }

    public function storeAnalysis(Request $request, string $threadId)
    {
        // 1. Auth & Validation
        $apiKey = $request->header('X-API-Key');
        if (!$apiKey) {
            return response()->json(['error' => 'Missing X-API-Key header'], 401);
        }

        $project = Project::where('api_key', $apiKey)->first();
        if (!$project) {
            return response()->json(['error' => 'Invalid API Key'], 401);
        }

        $thread = IssueThread::where('id', $threadId)->where('project_id', $project->id)->first();
        if (!$thread) {
            return response()->json(['error' => 'Thread not found or access denied'], 404);
        }

        $payload = $request->validate([
            'content' => 'required|string',
        ]);

        // 2. Create the AI Message
        $message = $thread->messages()->create([
            'sender_type' => 'ai_bot',
            'content' => $payload['content'],
            'created_at' => now(),
        ]);

        // 3. Update Thread Activity
        $thread->touch('latest_activity_at');

        // 4. Broadcast
        MessageCreated::dispatch($message);

        return response()->json($message, 201);
    }

    private function mapSeverity(string $level): string
    {
        $level = strtolower($level);
        return match ($level) {
            'critical', 'emergency', 'alert' => 'critical',
            'error' => 'high',
            'warning' => 'medium',
            default => 'low',
        };
    }
}
