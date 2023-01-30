@extends('layouts.app')

@section('content')

    <form class="auth-form " method="POST" action="{{ route('register') }}">
        @csrf

        <h1 class="form-title">Sign up to begin</h1>

        <div class="form-content">
            <div class="form-fields">
                <div class="group-form">
                    <label for="">Company name</label>
                    <input type="text" required name="name"  class="form-control  @error('name') is-invalid @enderror" />
                    @error('name')
                        <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">Company email</label>
                    <input type="email" required name="email"  class="form-control @error('email') is-invalid @enderror" />
                    @error('email')
                        <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">Investment amount</label>
                    <input type="number" required name="investment_amount"  class="form-control @error('investment_amount') is-invalid @enderror" />
                    @error('investment_amount')
                        <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">Location</label>
                    <input type="text" required name="location"  class="form-control @error('location') is-invalid @enderror" />
                    @error('location')
                        <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">ID registred company</label>
                    <input type="text" required class="form-control @error('register_company_id') is-invalid @enderror" name="register_company_id" />
                    @error('register_company_id')
                    <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
                </div>
                <div class="group-form">
                    <label for="">Password</label>
                    <input type="password" required name="password"  class="form-control @error('password')  is-invalid @enderror" />
                    @error('password')
                    <span class="invalid-feedback" role="alert">
                            {{ $message }}
                        </span>
                    @enderror
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
            <button  type="submit" class="btn submit">create AN ACCOUNT</button>
        </div>
    </form>

@endsection
