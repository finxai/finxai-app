<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FinXAi</title>
    <title>{{ config('app.name', 'Laravel') }}</title>
    <script src="{{ asset('js/app.js') }}" defer></script>
    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body class="auth">
<section class="auth-bg">
    <div class="auth-bg">
        <div class="header">
            <div class="header-logo">
                <div class="logo-image">finX<span>ai</span></div>
{{--                <img  src="{{asset('img/logo.svg')}}" alt="Logo">--}}
            </div>
            <h2 class="header-title">Portfolio Analysis</h2>
            <div class="header-links">w
                <a class="btn-outline" href="{{url("/#about")}}">About Us</a>
            </div>
        </div>
        <section class="auth-form">
            <img src="{{asset('img/rec-bg-img.png')}}" class="bg-image-right"></img>
            <img src="{{asset('img/vec-bg-img.png')}}" class="bg-image-left"></img>

            @yield('content')
        </section>
    </div>
</section>
</body>
</html>
