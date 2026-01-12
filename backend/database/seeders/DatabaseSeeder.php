<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // User::factory(10)->create();

        User::factory()->create([
            'name' => 'Demo User',
            'email' => 'admin@admin.com',
            'password' => 'password',
        ]);

        // Create a main project
        $project = \App\Models\Project::factory()->create([
            'name' => 'MyMind Main App',
        ]);

        // Create 20 bug threads for this project
        \Database\Factories\IssueThreadFactory::new()
            ->count(20)
            ->for($project)
            ->create()
            ->each(function ($thread) {
                // REQUIRED: First message is always the System Log (Issue details)
                \Database\Factories\ThreadMessageFactory::new()
                    ->state([
                        'sender_type' => 'system_log',
                        'content' => "Exception Trace:\n" . $thread->title . "\nStack trace:\n at App\Http\Controllers\Controller.php:45\n at Illuminate\Pipeline\Pipeline.php:120...",
                        'created_at' => $thread->created_at,
                    ])
                    ->for($thread, 'thread')
                    ->create();
            });
    }
}
