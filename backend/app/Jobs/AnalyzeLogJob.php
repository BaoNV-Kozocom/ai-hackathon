<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use App\Models\ThreadMessage;

class AnalyzeLogJob implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public ThreadMessage $message
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $message = $this->message;

        // Prevent infinite loops if AI analyzes its own message (though sender_type check prevents this)
        if ($message->sender_type !== 'system_log') {
            return;
        }

        // Call AI Service
        $aiService = new \App\Services\AiAnalysisService();
        $analysisResult = $aiService->analyze($message->content);

        // Create AI Message
        $aiMessage = $message->thread->messages()->create([
            'sender_type' => 'ai_bot',
            'content' => $analysisResult['analysis'],
            'meta_data' => [
                'has_actionable_fix' => true,
                'suggested_code' => $analysisResult['suggested_fix'],
                'file_path' => $analysisResult['file_path'],
                'confidence_score' => $analysisResult['confidence_score'],
                'diff_content' => $analysisResult['diff_content'] ?? null,
            ],
        ]);

        // Broadcast the new AI message
        \App\Events\MessageCreated::dispatch($aiMessage);
    }
}
