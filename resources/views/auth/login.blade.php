@extends('layouts.app')

@section('content')

    <form class="auth-form login" method="POST" action="{{ route('login') }}">
        @csrf

        <div class="form-content">

            <div class="form-fields">
                <h1 class="form-title">Log In to begin</h1>

                <div class="group-form">
                    <label for="">Company email</label>
                    <input type="email" name="email"  class="form-control @error('email') is-invalid @enderror" value="{{ old('email') }}" />
                    @error('email')
                    <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">Password</label>
                    <input type="password" name="password"  class="form-control @error('password')  is-invalid @enderror" />
                    @error('password')
                    <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>

                <div class="submit">
                    <button type="submit" class="btn submit">Log In</button>
                </div>
            </div>
            <div class="form-cta">
                <div class="cta-titles">
                    <h1>Welcome to FINXAI</h1>
                    <p>Fill up the information to start journey with us</p>
                </div>
                <div class="cta-action">
                    <p>Don’t have an account? </p>
                    <a class="btn-outline" href="{{route('register')}}">Sign Up</a>
                </div>
            </div>
        </div>


    </form>

@endsection
