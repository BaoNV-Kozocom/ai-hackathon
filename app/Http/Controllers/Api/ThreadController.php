<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\IssueThread;
use Illuminate\Http\Request;

class ThreadController extends Controller
{
    /**
     * List all threads.
     */
    public function index(Request $request)
    {
        $filter = $request->query('filter', 'all');

        $query = IssueThread::withCount('messages')
            ->orderBy('latest_activity_at', 'desc');

        if ($filter === 'open') {
            $query->where('status', 'open');
        } elseif ($filter === 'resolved') {
            $query->where('status', 'resolved');
        }

        $threads = $query->paginate(20);

        return response()->json($threads);
    }

    /**
     * Show a specific thread with messages.
     */
    public function show(string $id)
    {
        $thread = IssueThread::findOrFail($id);
        return response()->json($thread);
    }

    /**
     * Get messages for a specific thread.
     */
    public function messages(string $id)
    {
        $thread = IssueThread::findOrFail($id);
        return response()->json($thread->messages()->orderBy('created_at', 'asc')->get());
    }

    /**
     * Update thread status.
     */
    public function updateStatus(Request $request, string $id)
    {
        $thread = IssueThread::findOrFail($id);
        $validated = $request->validate([
            'status' => 'required|in:open,resolved,ignored',
        ]);

        $thread->update(['status' => $validated['status']]);

        return response()->json($thread);
    }

    /**
     * Store a new message in the thread.
     */
    public function storeMessage(Request $request, string $id)
    {
        $thread = IssueThread::findOrFail($id);
        $validated = $request->validate([
            'content' => 'required|string',
            'sender_type' => 'sometimes|in:human_user,ai_bot',
        ]);

        $message = $thread->messages()->create([
            'sender_type' => $validated['sender_type'] ?? 'human_user',
            'content' => $validated['content'],
            'created_at' => now(),
        ]);

        // Touch the thread to update latest_activity_at
        $thread->touch();

        return response()->json($message);
    }
}
