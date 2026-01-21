<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Support\Facades\Http;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        channels: __DIR__.'/../routes/channels.php',
        web: __DIR__ . '/../routes/web.php',
        api: __DIR__ . '/../routes/api.php',
        commands: __DIR__ . '/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        $middleware->statefulApi();
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        $exceptions->report(function (Throwable $exception) {
            $fullTrace = $exception->getTraceAsString();
            $traceLines = explode("\n", $fullTrace);
            $limitedTrace = implode("\n", array_slice($traceLines, 0, 15));
            
            // Capture error details
            $errorDetails = [
                'message' => $exception->getMessage(),
                'file' => $exception->getFile(),
                'line' => $exception->getLine(),
                'trace' => $limitedTrace,
                'code' => $exception->getCode(),
                'type' => get_class($exception),
                'timestamp' => now()->toIso8601String(),
            ];

            // Send error data to Python agent
            try {
                Http::timeout(5)->post('http://localhost:5001/analyze-error', $errorDetails);
            } catch (\Exception $e) {
                // Silently fail if the Python agent is not available
                // You can log this if needed: \Log::error('Failed to send error to Python agent: ' . $e->getMessage());
            }
        });
    })->create();
