<?php

use App\Http\Controllers\Api\IngestLogController;
use App\Http\Controllers\DemoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::post('/login', [\App\Http\Controllers\AuthController::class, 'login']);
Route::post('/logout', [\App\Http\Controllers\AuthController::class, 'logout'])->middleware('auth:sanctum');

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', [\App\Http\Controllers\AuthController::class, 'user']);
    Route::apiResource('threads', \App\Http\Controllers\Api\ThreadController::class)->only(['index', 'show']);
    Route::get('/threads/{id}/messages', [\App\Http\Controllers\Api\ThreadController::class, 'messages']);
    Route::post('/threads/{id}/messages', [\App\Http\Controllers\Api\ThreadController::class, 'storeMessage']);
    Route::patch('/threads/{id}/status', [\App\Http\Controllers\Api\ThreadController::class, 'updateStatus']);
});


Route::post('/ingest-log', [IngestLogController::class, 'store']);
Route::post('/ingest-analysis/{threadId}', [IngestLogController::class, 'storeAnalysis']);

Route::post('/demo/login-error', [DemoController::class, 'loginError']);
