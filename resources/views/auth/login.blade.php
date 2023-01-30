@extends('layouts.app')

@section('content')

    <form class="auth-form login">

        <div class="form-content">

            <div class="form-fields">
                <h1 class="form-title">Log In to begin</h1>

                <div class="group-form">
                    <label for="">Company email</label>
                    <input type="text" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">Password</label>
                    <input type="password" class="form-control" />
                </div>

                <div class="submit">
                    <button class="btn submit">Log In</button>
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
