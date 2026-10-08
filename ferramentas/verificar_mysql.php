<?php
require __DIR__.'/../sistema/vendor/autoload.php';
$app = require __DIR__.'/../sistema/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Illuminate\Support\Facades\DB;
use App\Models\{Produto,Movimentacao};
function verificar($condicao,$mensagem){if(!$condicao){throw new RuntimeException($mensagem);}echo "OK: $mensagem\n";}
$tabelas=DB::select('SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = ?', ['saep_db']);
verificar(count($tabelas)===3,'Exatamente três tabelas');
foreach($tabelas as $t){verificar($t->ENGINE==='InnoDB','InnoDB: '.$t->TABLE_NAME);}
$fks=DB::select('SELECT DELETE_RULE, UPDATE_RULE FROM information_schema.REFERENTIAL_CONSTRAINTS WHERE CONSTRAINT_SCHEMA = ?', ['saep_db']);
verificar(count($fks)===2,'Duas chaves estrangeiras');
foreach($fks as $fk){verificar($fk->DELETE_RULE==='RESTRICT' && $fk->UPDATE_RULE==='CASCADE','FK RESTRICT/CASCADE');}
$dados=json_decode(file_get_contents(__DIR__.'/../sistema/database/seeders/dados.json'),true);
foreach($dados as $tabela=>$rows){verificar(DB::table($tabela)->get()->map(fn($r)=>(array)$r)->all()==$rows,'Dados iguais ao SQL/seeder: '.$tabela);}
try {
 DB::transaction(function(){Produto::findOrFail(1)->update(['estoque'=>99]);Movimentacao::create(['produto_id'=>1,'usuario_id'=>1,'tipo'=>'entrada','quantidade'=>87,'data_movimentacao'=>'2026-10-07']);throw new RuntimeException('rollback de teste');});
}catch(RuntimeException $ex){if($ex->getMessage()!=='rollback de teste'){throw $ex;}}
verificar(Produto::find(1)->estoque===12 && Movimentacao::count()===3,'Rollback atômico de saldo e histórico no MySQL');
try {DB::transaction(fn()=>Produto::findOrFail(1)->delete());throw new RuntimeException('FK não bloqueou');}
catch(Illuminate\Database\QueryException $ex){verificar($ex->errorInfo[1]===1451,'MySQL bloqueia exclusão com histórico');}
