<?php

namespace Database\Factories;

use App\Models\IssueThread;
use App\Models\Project;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\IssueThread>
 */
class IssueThreadFactory extends Factory
{
    protected $model = IssueThread::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $exceptions = [
            "QueryException in OrderController",
            "NullReference in PaymentGateway",
            "MethodNotAllowedHttpException in API",
            "TimeoutException in ThirdPartyService",
            "ValidationException in RegistrationFlow",
            "AuthenticationException in LoginController",
            "BindingResolutionException in ServiceContainer",
            "ModelNotFoundException in CustomerController"
        ];

        $services = ["Checkout Service", "Auth Service", "Inventory Service", "Notification Service", "Payment Gateway"];

        return [
            'project_id' => Project::factory(),
            'title' => $this->faker->randomElement($exceptions),
            'error_hash' => md5($this->faker->unique()->sentence),
            'status' => $this->faker->randomElement(['open', 'resolved', 'ignored']),
            'severity' => $this->faker->randomElement(['low', 'medium', 'high', 'critical']),
            'source_service' => $this->faker->randomElement($services),
            'environment' => $this->faker->randomElement(['production', 'staging', 'development']),
            'latest_activity_at' => $this->faker->dateTimeBetween('-1 week', 'now'),
        ];
    }
}
