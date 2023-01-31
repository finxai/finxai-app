<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ config('app.name', 'Laravel') }}</title>
    <script src="{{ asset('js/app.js') }}" defer></script>
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body class="landing-page">
<section id="header">
    <div class="header">
        <nav class="nav">
            <div class="header-logo">
                <div class="logo-image">finX<span>ai</span></div>
{{--                <div class="logo-image"></div>--}}
            </div>
            <ul class="header-links">
                <li><a href="#about">about us</a></li>
                <li><a href="#team">team</a></li>
                <li><a href="#contact">contact</a></li>
            </ul>
            <a class="try-now" href="{{route('login')}}">TRY NOW</a>
        </nav>

        <div class="header-cta">

            <h1>Firms Portfolio Construction and Analysis
                <img src="{{asset('img/rec-bg-img.png')}}" class="header-cta-bg"/>
            </h1>
            <p>
                Lorem ipsum dolor sit amet consectetur. Magna laoreet vitae morbi ac
                libero tincidunt nam. Proin euismod adipiscing nisi.
            </p>
            <a href="{{route('login')}}">Try now</a>
        </div>
    </div>
</section>
<section id="about">
    <div class="about">
        <div class="about-content">
            <div class="about-title">
                <h2>about us</h2>
                <h1>Lorem ipsum dolor sit amet consectetur.</h1>
            </div>
            <div class="about-desc">
                <p>
                    Lorem ipsum dolor sit amet consectetur. Venenatis ultricies tellus
                    amet nunc risus facilisis. Id adipiscing duis morbi pharetra sit.
                    Dui amet morbi aliquam montes dolor lacus pharetra. Commodo amet
                    eu ultricies quam. Vitae tincidunt aliquam amet morbi. Hac dis
                    eget egestas duis.
                </p>
                <p>
                    Lorem ipsum dolor sit amet consectetur. Venenatis ultricies tellus
                    amet nunc risus facilisis. Id adipiscing duis morbi pharetra sit.
                </p>
                <div>
                    <a class="btn" {{route('login')}}>Try now</a>
                </div>
            </div>
        </div>
    </div>
    <section class="services">
        <div class="services">
            <h1>What we provide</h1>
            <div class="services-list">
                <div class="">
                    <h3>Lorem ipsum</h3>
                    <p>Lorem ipsum dolor sit amet consectetur.</p>
                </div>
                <div class="">
                    <h3>Lorem ipsum</h3>
                    <p>Lorem ipsum dolor sit amet consectetur.</p>
                </div>
                <div class="">
                    <h3>Lorem ipsum</h3>
                    <p>
                        Lorem ipsum dolor sit amet consectetur. Lorem ipsum dolor sit
                        amet consectetur.Lorem ipsum dolor sit amet consectetur.
                    </p>
                </div>
            </div>
        </div>
    </section>
</section>

<section id="team">
    <div class="team">
        <div class="team-titles">
            <h3>OUR TEAM</h3>
            <p>
                Lorem ipsum dolor sit amet consectetur. Venenatis ultricies tellus
                amet nunc risus facilisis. Id adipiscing duis morbi pharetra sit.
            </p>
        </div>
        <div class="team-members">
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>Edgar Hernandez Moto</h3>
                    <p>CEO in SEDLAXAR Technologies</p>
                </div>
            </div>
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>Asad Ali</h3>
                    <p>Artificial Intelligence Engineer</p>
                </div>
            </div>
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>AbdulQudus Yunus</h3>
                    <p>Software Engineer</p>
                </div>
            </div>
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>Huzaifa Zahoor</h3>
                    <p>Data Engineer</p>
                </div>
            </div>
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>Mohammed Ryayyan uddin</h3>
                    <p>CompSci sophmore</p>
                </div>
            </div>
            <div class="team-member">
                <div class="member-pic">
                    <div class="member-img"></div>
                </div>
                <div class="member-titles">
                    <h3>Anastasiya Viachorka</h3>
                    <p>UX/UI designer</p>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="contact">
    <div class="contact">
        <h3>Contact us</h3>
        <a href=""
        >contact@finxai.com
            <div></div
            ></a>
        <div class="contact-bg-gradient"></div>
    </div>
</section>
<section id="footer">
    <footer class="footer">
        <div class="header-logo">
            <div class="logo-image">finX<span>ai</span></div>
{{--            <div class="logo-image"></div>--}}
        </div>
        <ul class="header-links">
            <li><a href="#about">about us</a></li>
            <li><a href="#team">team</a></li>
            <li><a href="#contact">contact</a></li>
        </ul>
        <a class="try-now " href="{{route('login')}}">TRY NOW</a>
    </footer>
</section>
</body>
</html>
