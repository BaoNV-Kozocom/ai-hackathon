<?php

use Illuminate\Support\Facades\Broadcast;

Broadcast::channel('threads', function ($user) {
    return true;
});

Broadcast::channel('thread.{threadId}', function ($user, $threadId) {
    return true;
});
