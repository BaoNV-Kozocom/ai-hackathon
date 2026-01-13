<?php

namespace App\Services;

use App\Models\IssueThread;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class SlackNotificationService
{
    /**
     * Send a new issue notification to Slack
     *
     * @param IssueThread $thread
     * @return void
     */
    public function sendNewIssueNotification(IssueThread $thread): void
    {
        $webhookUrl = config('services.slack.webhook_url');
        $dashboardUrl = config('services.slack.dashboard_url');

        if (empty($webhookUrl)) {
            return;
        }

        $url = $dashboardUrl ? rtrim($dashboardUrl) . $thread->id : '';

        $payload = [
            'text' => $this->formatSlackMessage($thread->title, $url, $thread->severity, $thread->environment),
        ];

        try {
            Http::timeout(5)->post($webhookUrl, $payload);
        } catch (\Exception $e) {
            // Silently fail if Slack notification fails
            Log::error('Failed to send Slack notification: ' . $e->getMessage());
        }
    }

    /**
     * Format the Slack message
     *
     * @param string $title
     * @param string $url
     * @param string $severity
     * @param string $environment
     * @return string
     */
    private function formatSlackMessage(string $title, string $url, string $severity, string $environment): string
    {
        $icon = match ($severity) {
            'critical' => '🚨',
            'high' => '⚠️',
            'medium' => '⚡',
            default => '📝',
        };

        $message = "{$icon} New Issue Detected: {$title}\n\n";
        $message .= "Severity: {$severity}\n";
        $message .= "Environment: {$environment}\n";

        if ($url) {
            $message .= "View Details: {$url}";
        }

        return $message;
    }
}
