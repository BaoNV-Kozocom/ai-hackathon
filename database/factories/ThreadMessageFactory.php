<?php

namespace Database\Factories;

use App\Models\ThreadMessage;
use App\Models\IssueThread;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\ThreadMessage>
 */
class ThreadMessageFactory extends Factory
{
    protected $model = ThreadMessage::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $senderTypes = ['human_user', 'ai_bot', 'system_log'];
        $sender = $this->faker->randomElement($senderTypes);

        $metaData = null;
        if ($sender === 'ai_bot' && $this->faker->boolean(40)) {
            $metaData = [
                'suggested_code' => "if (!\$user) return response()->json(['error' => 'User not found'], 404);",
                'file_path' => "app/Http/Controllers/OrderController.php",
                'diff' => "- \$user->process();\n+ if (\$user) \$user->process();",
                'description' => "Added null check to prevent execution on null user object."
            ];
        }

        $content = match ($sender) {
            'human_user' => $this->faker->sentence(10),
            'ai_bot' => $this->faker->paragraph(2),
            'system_log' => "System alert: " . $this->faker->sentence(5),
            default => $this->faker->sentence
        };

        return [
            'issue_thread_id' => IssueThread::factory(),
            'sender_type' => $sender,
            'content' => $content,
            'meta_data' => $metaData ? $metaData : null, // Ensure encoding handled by cast
            'created_at' => $this->faker->dateTimeBetween('-1 week', 'now'),
        ];
    }
}
