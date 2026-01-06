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
        Schema::create('issue_threads', function (Blueprint $table) {
            $table->id();
            $table->foreignId('project_id')->constrained()->cascadeOnDelete();
            $table->string('title'); // e.g., "Generic Exception [CRITICAL] in PaymentService"
            $table->string('error_hash')->index(); // Unique hash of the error trace to group duplicates
            $table->enum('status', ['open', 'resolved', 'ignored'])->default('open')->index();
            $table->enum('severity', ['low', 'medium', 'high', 'critical'])->default('medium');
            $table->string('source_service')->nullable(); // e.g., "PaymentService-Worker-1"
            $table->string('environment')->default('production'); // local, staging, production
            $table->timestamp('latest_activity_at')->useCurrent();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('issue_threads');
    }
};
