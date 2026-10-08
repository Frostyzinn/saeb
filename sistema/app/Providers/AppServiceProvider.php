<?php

namespace App\Providers;

use App\Services\ArquivoMigrationRepository;
use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void {}

    public function boot(): void
    {
        // Carrega primeiro o provider diferido do Laravel para evitar sobrescrita do binding.
        $this->app->make('migration.repository');
        $this->app->singleton('migration.repository', fn () => new ArquivoMigrationRepository);
        Paginator::useBootstrapFive();
    }
}
