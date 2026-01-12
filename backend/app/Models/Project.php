<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Project extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'api_key',
        'repository_url',
        'webhook_secret',
    ];

    public function threads(): HasMany
    {
        return $this->hasMany(IssueThread::class);
    }
}
