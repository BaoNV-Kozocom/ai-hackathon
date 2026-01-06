<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class IssueThread extends Model
{
    use HasFactory;

    protected $fillable = [
        'project_id',
        'title',
        'error_hash',
        'status',
        'severity',
        'source_service',
        'environment',
        'latest_activity_at',
    ];

    protected $casts = [
        'latest_activity_at' => 'datetime',
    ];

    public function project(): BelongsTo
    {
        return $this->belongsTo(Project::class);
    }

    public function messages(): HasMany
    {
        return $this->hasMany(ThreadMessage::class);
    }
}
