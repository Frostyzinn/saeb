<?php

namespace App\Services;

use Illuminate\Database\Migrations\MigrationRepositoryInterface;
use Illuminate\Support\Facades\DB;

// Mantém o controle de migrations fora do banco, que deve conter só três tabelas.
class ArquivoMigrationRepository implements MigrationRepositoryInterface
{
    private $source;

    private array $memoria = [];

    private function path(): string
    {
        return storage_path('framework/migrations-'.md5((string) $this->source.config('database.connections.'.($this->source ?? config('database.default')).'.database')).'.json');
    }

    private function dados(): array
    {
        if (! DB::connection($this->source)->getSchemaBuilder()->hasTable('usuario')) {
            return [];
        }
        if (app()->environment('testing')) {
            return $this->memoria;
        }

        return is_file($this->path()) ? json_decode(file_get_contents($this->path()), true, 512, JSON_THROW_ON_ERROR) : [];
    }

    private function gravar(array $dados): void
    {
        if (app()->environment('testing')) {
            $this->memoria = $dados;
        } else {
            file_put_contents($this->path(), json_encode($dados, JSON_THROW_ON_ERROR), LOCK_EX);
        }
    }

    public function getRan()
    {
        return array_keys($this->dados());
    }

    public function getMigrationBatches()
    {
        return $this->dados();
    }

    public function getMigrations($steps)
    {
        return array_slice($this->registros(), 0, $steps);
    }

    public function getMigrationsByBatch($batch)
    {
        return array_values(array_filter($this->registros(), fn ($r) => $r->batch == $batch));
    }

    private function registros(): array
    {
        $r = [];
        foreach (array_reverse($this->dados(), true) as $m => $b) {
            $r[] = (object) ['migration' => $m, 'batch' => $b];
        }

        return $r;
    }

    public function getLast()
    {
        return $this->getMigrationsByBatch($this->getLastBatchNumber());
    }

    public function getLastBatchNumber()
    {
        return max([0, ...array_values($this->dados())]);
    }

    public function getNextBatchNumber()
    {
        return $this->getLastBatchNumber() + 1;
    }

    public function log($file, $batch)
    {
        $dados = $this->dados();
        $dados[$file] = $batch;
        $this->gravar($dados);
    }

    public function delete($migration)
    {
        $dados = $this->dados();
        unset($dados[$migration->migration]);
        $this->gravar($dados);
    }

    public function createRepository()
    {
        $this->gravar([]);
    }

    public function repositoryExists()
    {
        return DB::connection($this->source)->getSchemaBuilder()->hasTable('usuario');
    }

    public function deleteRepository()
    {
        if (! app()->environment('testing') && is_file($this->path())) {
            unlink($this->path());
        }
        $this->memoria = [];
    }

    public function setSource($name)
    {
        $this->source = $name;
    }
}
