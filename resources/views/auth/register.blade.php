@extends('layouts.app')

@section('content')

    <form class="auth-form ">
        <h1 class="form-title">Sign up to begin</h1>

        <div class="form-content">
            <div class="form-fields">
                <div class="group-form">
                    <label for="">Company name</label>
                    <input type="text" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">Company email</label>
                    <input type="text" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">Investment amount</label>
                    <input type="number" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">Location</label>
                    <input type="text" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">ID registred company</label>
                    <input type="text" class="form-control" />
                </div>
                <div class="group-form">
                    <label for="">Password</label>
                    <input type="password" class="form-control" />
                </div>
            </div>
            <div class="form-cta">
                <div class="cta-titles">
                    <h1>Welcome to FINXAI</h1>
                    <p>Fill up the information to start journey with us</p>
                </div>
                <div class="cta-action">
                    <p>Already have an account? </p>
                    <a class="btn-outline" href="{{route('login')}}">Log In</a>
                </div>
            </div>
        </div>

        <div class="submit">
            <button class="btn submit">create AN ACCOUNT</button>
        </div>
    </form>

@endsection
