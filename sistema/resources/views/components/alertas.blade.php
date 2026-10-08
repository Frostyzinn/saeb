@foreach(['success'=>'success','warning'=>'warning','error'=>'danger'] as $chave=>$cor)
@if(session($chave))<div role="alert" class="alert alert-{{ $cor }} {{ $chave==='warning'?'border border-danger border-2 fw-bold':'' }}">{{ session($chave) }}</div>@endif
@endforeach
@if($errors->any())<div role="alert" class="alert alert-danger"><strong>Confira os dados informados:</strong><ul class="mb-0">@foreach($errors->all() as $erro)<li>{{ $erro }}</li>@endforeach</ul></div>@endif
