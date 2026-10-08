from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
s=root/'sistema'
def put(path,text):
 p=s/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
for p in (s/'database/migrations').glob('*.php'): p.unlink()
for p in ['app/Models/User.php','database/factories/UserFactory.php','tests/Feature/ExampleTest.php','tests/Unit/ExampleTest.php']:
 (s/p).unlink(missing_ok=True)
put('database/migrations/2026_01_01_000000_criar_estoque.php',r'''<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration {
 public function up(): void {
  Schema::create('usuario',function(Blueprint $t){$t->increments('idusuario');$t->string('name',100);$t->string('email',100)->unique();$t->string('password',255);});
  Schema::create('produtos',function(Blueprint $t){$t->increments('id');$t->string('nome',100);$t->string('marca',60);$t->string('modelo',60);$t->string('material',60);$t->string('tamanho',30);$t->decimal('peso',8,2);$t->string('tensao',30);$t->integer('estoque')->default(0);$t->integer('estoque_minimo')->default(0);});
  Schema::create('movimentacoes',function(Blueprint $t){$t->increments('id');$t->unsignedInteger('produto_id');$t->unsignedInteger('usuario_id');$t->enum('tipo',['entrada','saida']);$t->integer('quantidade');$t->date('data_movimentacao');$t->foreign('produto_id')->references('id')->on('produtos')->restrictOnDelete()->cascadeOnUpdate();$t->foreign('usuario_id')->references('idusuario')->on('usuario')->restrictOnDelete()->cascadeOnUpdate();});
 }
 public function down(): void {Schema::dropIfExists('movimentacoes');Schema::dropIfExists('produtos');Schema::dropIfExists('usuario');}
};''')
put('app/Models/Usuario.php',r'''<?php
namespace App\Models;
use Illuminate\Foundation\Auth\User as Authenticatable;
class Usuario extends Authenticatable {
 protected $table='usuario'; protected $primaryKey='idusuario'; public $timestamps=false;
 protected $fillable=['name','email','password']; protected $hidden=['password'];
 protected function casts(): array {return ['password'=>'hashed'];}
 public function getRememberTokenName(){return '';}
 public function movimentacoes(){return $this->hasMany(Movimentacao::class,'usuario_id','idusuario');}
}''')
put('app/Models/Produto.php',r'''<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class Produto extends Model {
 protected $table='produtos'; public $timestamps=false;
 protected $fillable=['nome','marca','modelo','material','tamanho','peso','tensao','estoque','estoque_minimo'];
 protected function casts(): array {return ['peso'=>'decimal:2','estoque'=>'integer','estoque_minimo'=>'integer'];}
 public function movimentacoes(){return $this->hasMany(Movimentacao::class);}
 public function abaixoDoMinimo(): bool {return $this->estoque < $this->estoque_minimo;}
 public function scopeBuscar($query,$termo){return $query->when($termo !== null && $termo !== '',fn($q)=>$q->where(function($q)use($termo){foreach(['nome','marca','modelo','material'] as $campo){$q->orWhere($campo,'like','%'.$termo.'%');}}));}
}''')
put('app/Models/Movimentacao.php',r'''<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class Movimentacao extends Model {
 protected $table='movimentacoes';public $timestamps=false;
 protected $fillable=['produto_id','usuario_id','tipo','quantidade','data_movimentacao'];
 protected function casts(): array{return ['data_movimentacao'=>'date','quantidade'=>'integer'];}
 public function produto(){return $this->belongsTo(Produto::class);}
 public function usuario(){return $this->belongsTo(Usuario::class,'usuario_id','idusuario');}
}''')
p=s/'config/auth.php';p.write_text(p.read_text().replace('App\\Models\\User::class','App\\Models\\Usuario::class'),encoding='utf-8')
put('app/Services/OrdenacaoService.php',r'''<?php
namespace App\Services;
use Illuminate\Support\Collection;
use Illuminate\Support\Str;
class OrdenacaoService {
 public function ordenar(Collection $produtos): Collection {
  $itens=$produtos->all();
  // Insertion Sort: desloca os maiores à direita e insere o elemento na posição correta.
  for($i=1;$i<count($itens);$i++){
   $atual=$itens[$i];$chave=$this->normalizar($atual->nome);$j=$i-1;
   while($j>=0 && strcmp($this->normalizar($itens[$j]->nome),$chave)>0){$itens[$j+1]=$itens[$j];$j--;}
   $itens[$j+1]=$atual;
  }
  return collect($itens);
 }
 private function normalizar(string $nome): string{return Str::ascii(mb_strtolower($nome,'UTF-8'));}
}''')
put('app/Http/Requests/ProdutoRequest.php',r'''<?php
namespace App\Http\Requests;
use Illuminate\Foundation\Http\FormRequest;
class ProdutoRequest extends FormRequest {
 public function authorize(): bool{return true;}
 public function rules(): array {
  $r=[];foreach(['nome'=>100,'marca'=>60,'modelo'=>60,'material'=>60,'tamanho'=>30,'tensao'=>30] as $c=>$n){$r[$c]=['required','string','max:'.$n];}
  return $r+['peso'=>['required','numeric','min:0','max:999999.99'],'estoque'=>['required','integer','min:0','max:2147483647'],'estoque_minimo'=>['required','integer','min:0','max:2147483647']];
 }
 public function messages(): array{return ['required'=>'O campo :attribute é obrigatório.','string'=>'O campo :attribute deve ser um texto.','max'=>'O campo :attribute excede o limite permitido (:max).','numeric'=>'O campo :attribute deve ser numérico.','integer'=>'O campo :attribute deve ser inteiro.','min'=>'O campo :attribute deve ser pelo menos :min.'];}
 public function attributes(): array{return ['tensao'=>'tensão','estoque_minimo'=>'estoque mínimo'];}
}''')
put('app/Http/Requests/MovimentacaoRequest.php',r'''<?php
namespace App\Http\Requests;
use Illuminate\Foundation\Http\FormRequest;
class MovimentacaoRequest extends FormRequest {
 public function authorize(): bool{return true;}
 public function rules(): array{return ['produto_id'=>'required|integer|exists:produtos,id','tipo'=>'required|in:entrada,saida','quantidade'=>'required|integer|min:1|max:2147483647','data_movimentacao'=>'required|date_format:Y-m-d|before_or_equal:today'];}
 public function messages(): array{return ['required'=>'O campo :attribute é obrigatório.','integer'=>'O campo :attribute deve ser inteiro.','exists'=>'Selecione um produto existente.','in'=>'Selecione entrada ou saída.','min'=>'A quantidade deve ser pelo menos 1.','max'=>'A quantidade excede o limite permitido.','date_format'=>'Informe uma data válida.','before_or_equal'=>'A data não pode ser futura.'];}
 public function attributes(): array{return ['produto_id'=>'produto','data_movimentacao'=>'data da movimentação'];}
}''')
put('app/Http/Controllers/AuthController.php',r'''<?php
namespace App\Http\Controllers;
use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\{Auth,Hash};
class AuthController extends Controller {
 public function login(){return view('auth.login');}
 public function autenticar(Request $r){
  if(!is_string($r->email)||!is_string($r->password)||trim($r->email)===''||$r->password===''){return back()->withErrors(['email'=>'Preencha e-mail e senha'])->withInput($r->only('email'));}
  $u=Usuario::where('email',$r->email)->first();
  if(!$u){return back()->withErrors(['email'=>'E-mail não cadastrado'])->withInput($r->only('email'));}
  if(!Hash::check($r->password,$u->password)){return back()->withErrors(['password'=>'Senha incorreta'])->withInput($r->only('email'));}
  Auth::login($u);$r->session()->regenerate();return redirect()->intended(route('home'));
 }
 public function logout(Request $r){Auth::logout();$r->session()->invalidate();$r->session()->regenerateToken();return redirect()->route('login');}
}''')
put('app/Http/Controllers/HomeController.php',r'''<?php
namespace App\Http\Controllers;
use App\Models\{Produto,Movimentacao};
class HomeController extends Controller {
 public function index(){return view('home',['total'=>Produto::count(),'alertas'=>Produto::whereColumn('estoque','<','estoque_minimo')->count(),'movimentos'=>Movimentacao::count()]);}
}''')
put('app/Http/Controllers/ProdutoController.php',r'''<?php
namespace App\Http\Controllers;
use App\Models\Produto;
use App\Http\Requests\ProdutoRequest;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
class ProdutoController extends Controller {
 public function index(Request $r){$termo=$r->string('busca')->toString();return view('produtos.index',['produtos'=>Produto::buscar($termo)->get(),'termo'=>$termo]);}
 public function create(){return view('produtos.form',['produto'=>new Produto]);}
 public function edit(Produto $produto){return view('produtos.form',compact('produto'));}
 public function store(ProdutoRequest $r){Produto::create($r->validated());return redirect()->route('produtos.index')->with('success','Produto cadastrado com sucesso.');}
 public function update(ProdutoRequest $r,Produto $produto){$produto->update($r->validated());return redirect()->route('produtos.index')->with('success','Produto atualizado com sucesso.');}
 public function destroy(Produto $produto){
  DB::transaction(function()use($produto){$p=Produto::lockForUpdate()->findOrFail($produto->id);if($p->movimentacoes()->exists()){throw ValidationException::withMessages(['produto'=>'Não é possível excluir um produto com movimentações. O histórico deve ser preservado.']);}$p->delete();});
  return redirect()->route('produtos.index')->with('success','Produto excluído com sucesso.');
 }
}''')
put('app/Http/Controllers/EstoqueController.php',r'''<?php
namespace App\Http\Controllers;
use App\Models\{Produto,Movimentacao};
use App\Http\Requests\MovimentacaoRequest;
use App\Services\OrdenacaoService;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
class EstoqueController extends Controller {
 public function index(OrdenacaoService $ordenacao){return view('estoque.index',['produtos'=>$ordenacao->ordenar(Produto::all()),'historico'=>Movimentacao::with(['produto','usuario'])->orderByDesc('data_movimentacao')->orderByDesc('id')->paginate(20)]);}
 public function registrar(MovimentacaoRequest $r){
  $alerta=DB::transaction(function()use($r){
   $p=Produto::lockForUpdate()->findOrFail($r->validated('produto_id'));$q=(int)$r->validated('quantidade');$tipo=$r->validated('tipo');
   if($tipo==='saida' && $q>$p->estoque){throw ValidationException::withMessages(['quantidade'=>'Saída maior que o estoque disponível ('.$p->estoque.').']);}
   $novo=$p->estoque+($tipo==='entrada'?$q:-$q);
   if($novo>2147483647){throw ValidationException::withMessages(['quantidade'=>'A entrada ultrapassa o limite de estoque.']);}
   Movimentacao::create($r->validated()+['usuario_id'=>$r->user()->idusuario]);$p->update(['estoque'=>$novo]);
   return $tipo==='saida' && $p->abaixoDoMinimo()?"Atenção: o estoque de {$p->nome} ficou em {$p->estoque}, abaixo do mínimo de {$p->estoque_minimo}":null;
  });
  return redirect()->route('estoque.index')->with('success','Movimentação registrada com sucesso.')->with('warning',$alerta);
 }
}''')
put('routes/web.php',r'''<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\{AuthController,HomeController,ProdutoController,EstoqueController};
Route::middleware('guest')->group(function(){Route::get('/login',[AuthController::class,'login'])->name('login');Route::post('/login',[AuthController::class,'autenticar'])->middleware('throttle:10,1')->name('login.autenticar');});
Route::middleware('auth')->group(function(){
 Route::get('/',[HomeController::class,'index'])->name('home');Route::post('/logout',[AuthController::class,'logout'])->name('logout');
 Route::resource('produtos',ProdutoController::class)->except('show');
 Route::get('/estoque',[EstoqueController::class,'index'])->name('estoque.index');Route::post('/estoque',[EstoqueController::class,'registrar'])->name('estoque.registrar');
});''')
put('resources/views/layouts/app.blade.php',r'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>@yield('title', 'SAEP • Almoxarifado')</title><link href="{{ asset('css/bootstrap.min.css') }}" rel="stylesheet"><link href="{{ asset('css/app.css') }}" rel="stylesheet"></head>
<body><nav class="navbar navbar-dark"><div class="container"><a class="navbar-brand fw-bold" href="{{ route('home') }}">SAEP <span class="fw-normal">/ Almoxarifado</span></a>@auth<div class="d-flex align-items-center gap-3 text-white"><span>{{ auth()->user()->name }}</span><form method="post" action="{{ route('logout') }}">@csrf<button class="btn btn-outline-light btn-sm">Sair</button></form></div>@endauth</div></nav><main class="container py-5"><x-alertas/>@yield('content')</main><footer class="container py-4 text-secondary small">SAEP / SENAI · Controle de ferramentas e materiais</footer></body></html>''')
put('resources/views/components/alertas.blade.php',r'''@foreach(['success'=>'success','warning'=>'warning','error'=>'danger'] as $chave=>$cor)
@if(session($chave))<div role="alert" class="alert alert-{{ $cor }} {{ $chave==='warning'?'border border-danger border-2 fw-bold':'' }}">{{ session($chave) }}</div>@endif
@endforeach
@if($errors->any())<div role="alert" class="alert alert-danger"><strong>Confira os dados informados:</strong><ul class="mb-0">@foreach($errors->all() as $erro)<li>{{ $erro }}</li>@endforeach</ul></div>@endif''')
put('resources/views/auth/login.blade.php',r'''@extends('layouts.app')
@section('content')<div class="row justify-content-center"><div class="col-md-6 col-lg-4"><div class="card p-4"><span class="eyebrow">ACESSO AO SISTEMA</span><h1 class="h3 mt-2">Bem-vindo ao almoxarifado</h1><p class="text-secondary">Entre para acompanhar seus produtos e movimentações.</p><form method="post" action="{{ route('login.autenticar') }}">@csrf<div class="mb-3"><label for="email" class="form-label">E-mail</label><input id="email" name="email" type="email" autocomplete="username" value="{{ old('email') }}" class="form-control @error('email') is-invalid @enderror">@error('email')<div class="invalid-feedback">{{ $message }}</div>@enderror</div><div class="mb-4"><label for="password" class="form-label">Senha</label><input id="password" name="password" type="password" autocomplete="current-password" class="form-control @error('password') is-invalid @enderror">@error('password')<div class="invalid-feedback">{{ $message }}</div>@enderror</div><button class="btn btn-primary w-100">Entrar</button></form></div></div></div>@endsection''')
put('resources/views/home.blade.php',r'''@extends('layouts.app')
@section('content')<span class="eyebrow">PAINEL DO ALMOXARIFADO</span><h1 class="mt-2">Olá, {{ auth()->user()->name }}.</h1><p class="text-secondary mb-4">Organize suas ferramentas. Acompanhe cada movimento.</p><div class="row g-3 mb-5">@foreach(['Produtos cadastrados'=>$total,'Abaixo do estoque mínimo'=>$alertas,'Movimentações registradas'=>$movimentos] as $label=>$valor)<div class="col-md-4"><div class="card p-4"><div class="display-5 fw-bold">{{ $valor }}</div><span class="text-secondary">{{ $label }}</span></div></div>@endforeach</div><div class="row g-4"><div class="col-md-6"><a class="card p-4 action-card" href="{{ route('produtos.index') }}"><h2 class="h4">Cadastro de Produto →</h2><p class="mb-0">Consulte, cadastre e atualize o catálogo de ferramentas.</p></a></div><div class="col-md-6"><a class="card p-4 action-card" href="{{ route('estoque.index') }}"><h2 class="h4">Gestão de Estoque →</h2><p class="mb-0">Registre entradas e saídas e consulte o histórico.</p></a></div></div>@endsection''')
put('resources/views/produtos/index.blade.php',r'''@extends('layouts.app')
@section('content')<a href="{{ route('home') }}" class="back">← Voltar à interface principal</a><div class="d-flex flex-wrap justify-content-between gap-3 my-4"><h1>Cadastro de Produto</h1><a href="{{ route('produtos.create') }}" class="btn btn-primary align-self-center">+ Novo produto</a></div><form class="d-flex gap-2 mb-4" method="get" action="{{ route('produtos.index') }}"><label class="visually-hidden" for="busca">Buscar produtos</label><input class="form-control" id="busca" name="busca" value="{{ $termo }}" placeholder="Busque por nome, marca, modelo ou material"><button class="btn btn-primary">Buscar</button><a class="btn btn-outline-secondary text-nowrap" href="{{ route('produtos.index') }}">Limpar busca</a></form><div class="card table-responsive"><table class="table align-middle mb-0"><thead><tr><th>Produto</th><th>Marca / modelo</th><th>Material</th><th>Tamanho</th><th>Peso (kg)</th><th>Tensão</th><th>Estoque / mínimo</th><th>Ações</th></tr></thead><tbody>@forelse($produtos as $p)<tr><td class="fw-bold">{{ $p->nome }}</td><td>{{ $p->marca }} / {{ $p->modelo }}</td><td>{{ $p->material }}</td><td>{{ $p->tamanho }}</td><td>{{ number_format((float)$p->peso,2,',','.') }}</td><td>{{ $p->tensao }}</td><td>{{ $p->estoque }} / {{ $p->estoque_minimo }}</td><td><div class="d-flex gap-2"><a class="btn btn-sm btn-outline-primary" href="{{ route('produtos.edit',$p) }}">Editar</a><form method="post" action="{{ route('produtos.destroy',$p) }}" onsubmit="return confirm('Confirma a exclusão deste produto?')">@csrf @method('DELETE')<button class="btn btn-sm btn-outline-danger">Excluir</button></form></div></td></tr>@empty<tr><td colspan="8" class="text-center py-5">Nenhum produto encontrado</td></tr>@endforelse</tbody></table></div>@endsection''')
put('resources/views/produtos/form.blade.php',r'''@extends('layouts.app')
@section('content')<a class="back" href="{{ route('produtos.index') }}">← Voltar ao cadastro</a><h1 class="my-4">{{ $produto->exists?'Editar produto':'Novo produto' }}</h1><form class="card p-4" method="post" action="{{ $produto->exists?route('produtos.update',$produto):route('produtos.store') }}">@csrf @if($produto->exists) @method('PUT') @endif<div class="row g-3">@foreach(['nome'=>'Nome','marca'=>'Marca','modelo'=>'Modelo','material'=>'Material','tamanho'=>'Tamanho','peso'=>'Peso (kg)','tensao'=>'Tensão','estoque'=>'Estoque','estoque_minimo'=>'Estoque mínimo'] as $campo=>$label)<div class="col-md-{{ $campo==='nome'?12:6 }}"><label class="form-label" for="{{ $campo }}">{{ $label }}</label><input required id="{{ $campo }}" name="{{ $campo }}" class="form-control @error($campo) is-invalid @enderror" value="{{ old($campo,$produto->$campo ?? (in_array($campo,['estoque','estoque_minimo'])?0:'')) }}" @if(in_array($campo,['peso','estoque','estoque_minimo'])) type="number" min="0" step="{{ $campo==='peso'?'0.01':'1' }}" @else type="text" maxlength="{{ ['nome'=>100,'marca'=>60,'modelo'=>60,'material'=>60,'tamanho'=>30,'tensao'=>30][$campo] }}" @endif>@error($campo)<div class="invalid-feedback">{{ $message }}</div>@enderror</div>@endforeach</div><div class="mt-4 d-flex gap-2"><button class="btn btn-primary">Salvar produto</button><a class="btn btn-outline-secondary" href="{{ route('produtos.index') }}">Cancelar</a><a class="btn btn-link" href="{{ route('home') }}">Interface principal</a></div></form>@endsection''')
put('resources/views/estoque/index.blade.php',r'''@extends('layouts.app')
@section('content')<a class="back" href="{{ route('home') }}">← Voltar à interface principal</a><h1 class="my-4">Gestão de Estoque</h1><div class="row g-4"><div class="col-lg-4"><form class="card p-4" method="post" action="{{ route('estoque.registrar') }}">@csrf<h2 class="h5 mb-4">Registrar movimentação</h2><label class="form-label" for="produto_id">Produto</label><select required class="form-select @error('produto_id') is-invalid @enderror" name="produto_id" id="produto_id"><option value="">Selecione um produto</option>@foreach($produtos as $p)<option value="{{ $p->id }}" @selected(old('produto_id')==$p->id)>{{ $p->nome }} ({{ $p->estoque }} disponíveis)</option>@endforeach</select>@error('produto_id')<div class="invalid-feedback">{{ $message }}</div>@enderror<fieldset class="my-3"><legend class="fs-6">Tipo de movimentação</legend>@foreach(['entrada'=>'Entrada','saida'=>'Saída'] as $tipo=>$label)<div class="form-check form-check-inline"><input required class="form-check-input" id="{{ $tipo }}" name="tipo" type="radio" value="{{ $tipo }}" @checked(old('tipo','entrada')===$tipo)><label class="form-check-label" for="{{ $tipo }}">{{ $label }}</label></div>@endforeach @error('tipo')<p class="text-danger small">{{ $message }}</p>@enderror</fieldset>@foreach(['quantidade'=>'Quantidade','data_movimentacao'=>'Data da movimentação'] as $campo=>$label)<div class="mb-3"><label class="form-label" for="{{ $campo }}">{{ $label }}</label><input required class="form-control @error($campo) is-invalid @enderror" id="{{ $campo }}" name="{{ $campo }}" type="{{ $campo==='quantidade'?'number':'date' }}" value="{{ old($campo,$campo==='quantidade'?1:now()->format('Y-m-d')) }}" @if($campo==='quantidade') min="1" step="1" @else max="{{ now()->format('Y-m-d') }}" @endif>@error($campo)<div class="invalid-feedback">{{ $message }}</div>@enderror</div>@endforeach<button class="btn btn-primary mt-2">Registrar movimentação</button></form></div><div class="col-lg-8"><div class="card table-responsive"><table class="table mb-0"><thead><tr><th>Produto</th><th>Estoque</th><th>Mínimo</th><th>Situação</th></tr></thead><tbody>@forelse($produtos as $p)<tr><td>{{ $p->nome }}</td><td>{{ $p->estoque }}</td><td>{{ $p->estoque_minimo }}</td><td><span class="badge text-bg-{{ $p->abaixoDoMinimo()?'danger':'success' }}">{{ $p->abaixoDoMinimo()?'Abaixo do mínimo':'Regular' }}</span></td></tr>@empty<tr><td colspan="4">Nenhum produto cadastrado</td></tr>@endforelse</tbody></table></div></div></div><h2 class="h4 mt-5 mb-3">Histórico de movimentações</h2><div class="card table-responsive"><table class="table mb-0"><thead><tr><th>Data</th><th>Produto</th><th>Tipo</th><th>Quantidade</th><th>Responsável</th></tr></thead><tbody>@forelse($historico as $m)<tr><td>{{ $m->data_movimentacao->format('d/m/Y') }}</td><td>{{ $m->produto->nome }}</td><td>{{ $m->tipo==='entrada'?'Entrada':'Saída' }}</td><td>{{ $m->quantidade }}</td><td>{{ $m->usuario->name }}</td></tr>@empty<tr><td colspan="5">Nenhuma movimentação registrada</td></tr>@endforelse</tbody></table></div><div class="mt-3">{{ $historico->links() }}</div>@endsection''')
put('public/css/app.css','''body{background:#f3f6f9;color:#172d40;font-family:system-ui,sans-serif}.navbar{background:#102d43;padding:18px 0}.navbar-brand span{font-size:15px;color:#a4c0d2}.card{border:1px solid #dde5ed;border-radius:14px;box-shadow:0 4px 16px #102d4306}.btn-primary{background:#087e8b;border-color:#087e8b}.btn-primary:hover{background:#05616b;border-color:#05616b}.eyebrow{color:#087e8b;font-weight:700;letter-spacing:2px;font-size:12px}.action-card{text-decoration:none;color:inherit;transition:transform .2s}.action-card:hover{transform:translateY(-3px);border-color:#087e8b}.table th{background:#edf3f6;color:#526678;font-size:13px;padding:16px}.table td{padding:16px}.back{color:#087e8b;text-decoration:none}h1{font-weight:750;letter-spacing:-1px;font-size:32px}''')
p=s/'app/Providers/AppServiceProvider.php';t=p.read_text().replace('//',r'\Illuminate\Pagination\Paginator::useBootstrapFive();',1);p.write_text(t,encoding='utf-8')
p=s/'config/app.php';t=p.read_text().replace("'timezone' => 'UTC'","'timezone' => 'America/Sao_Paulo'").replace("env('APP_LOCALE', 'en')","env('APP_LOCALE', 'pt_BR')");p.write_text(t,encoding='utf-8')
env='''APP_NAME="SAEP Almoxarifado"
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://127.0.0.1:8000
APP_LOCALE=pt_BR
APP_FALLBACK_LOCALE=pt_BR
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=saep_db
DB_USERNAME=root
DB_PASSWORD=
SESSION_DRIVER=file
CACHE_STORE=file
QUEUE_CONNECTION=sync
LOG_CHANNEL=single
'''
put('.env',env);put('.env.example',env)
p=s/'phpunit.xml';t=p.read_text().replace('<!-- <env name="DB_CONNECTION" value="sqlite"/> -->','<env name="DB_CONNECTION" value="sqlite" force="true"/>').replace('<!-- <env name="DB_DATABASE" value=":memory:"/> -->','<env name="DB_DATABASE" value=":memory:" force="true"/>');p.write_text(t,encoding='utf-8')
print('Código gerado.')
