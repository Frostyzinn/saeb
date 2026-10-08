<?php

namespace App\Http\Controllers;

use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function login()
    {
        return view('auth.login');
    }

    public function autenticar(Request $r)
    {
        if (! is_string($r->email) || ! is_string($r->password) || trim($r->email) === '' || $r->password === '') {
            return back()->withErrors(['email' => 'Preencha e-mail e senha'])->withInput($r->only('email'));
        }
        $u = Usuario::where('email', $r->email)->first();
        if (! $u) {
            return back()->withErrors(['email' => 'E-mail não cadastrado'])->withInput($r->only('email'));
        }
        if (! Hash::check($r->password, $u->password)) {
            return back()->withErrors(['password' => 'Senha incorreta'])->withInput($r->only('email'));
        }
        Auth::login($u);
        $r->session()->regenerate();

        return redirect()->intended(route('home'));
    }

    public function logout(Request $r)
    {
        Auth::logout();
        $r->session()->invalidate();
        $r->session()->regenerateToken();

        return redirect()->route('login');
    }
}
