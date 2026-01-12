<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('thread_messages', function (Blueprint $table) {
            $table->id();
            $table->foreignId('issue_thread_id')->constrained('issue_threads')->cascadeOnDelete();
            $table->enum('sender_type', ['system_log', 'ai_bot', 'human_user']);
            $table->text('content'); // The message text or raw log
            $table->json('meta_data')->nullable(); // Structured data: actionable items, code diffs, file paths
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('thread_messages');
    }
};
