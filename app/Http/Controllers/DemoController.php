<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class DemoController extends Controller
{
    /**
     * Trigger a critical error for demonstration purposes.
     */
    public function loginError(Request $request)
    {
        $email = $request->input('email') ?? 'unknown@example.com';
        $userProfile = $this->getUserProfile($email);

        if (!$userProfile) {
            return response()->json([
                'status' => 'error',
                'message' => 'User not found.'
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => $userProfile->toArray()
        ]);
    }
    /**
     * Simulate a database query that fails to find the record
     *
     * @param string $email
     * @return User|null
     */
    private function getUserProfile($email): ?User
    {
        return User::select('id', 'name', 'email')->where('email', $email)->first();
    }
}
