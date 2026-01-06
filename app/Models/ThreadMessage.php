<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class ThreadMessage extends Model
{
    use HasFactory;

    protected $fillable = [
        'issue_thread_id',
        'sender_type',
        'content',
        'meta_data',
    ];

    protected $casts = [
        'meta_data' => 'array',
    ];

    public function thread(): BelongsTo
    {
        return $this->belongsTo(IssueThread::class, 'issue_thread_id');
    }
}
