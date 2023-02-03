<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FinXAi - Result</title>
    <title>{{ config('app.name', 'Laravel') }}</title>
    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body class="result">

    <section  id="app" class="results">

        <div class="left details">

            <div class="header-logo">
                <div class="logo-image">finX<span>ai</span></div>
            </div>

            <div class="account">
                <div class="account-pic">
                   <img src="{{asset('img/header.png')}}" alt="Logo">
                </div>
                <div class="info">
                    <div class="info-item">
                        <h4>Account number</h4>
                        <h5>PA2O8U7QKFPG</h5>
                    </div>
                    <div class="info-item">
                        <h4>Status</h4>
                        <h5>ACTIVE</h5>
                    </div>
                </div>
            </div>
            <div class="details-box">

                <h5 class="details-header">Details</h5>

                <div class="details-items">

                    <div class="details-item">
                        <h5>Buying power</h5>
                        <h6>200000</h6>
                    </div>
                    <div class="details-item">
                        <h5>Non marginable buying power</h5>
                        <h6>98000</h6>
                    </div>
                    <div class="details-item">
                        <h5>Accrued fees</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Pending transfer out</h5>
                        <h6>None</h6>
                    </div>
                    <div class="details-item">
                        <h5>Pending transfer in</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Portfolio value</h5>
                        <h6>100000</h6>
                    </div>
                    <div class="details-item">
                        <h5>Multiplier</h5>
                        <h6>2</h6>
                    </div>
                    <div class="details-item">
                        <h5>Shorting enabled</h5>
                        <h6>True</h6>
                    </div>
                    <div class="details-item">
                        <h5>Equity</h5>
                        <h6>100000</h6>
                    </div>
                    <div class="details-item">
                        <h5>Ast Equity</h5>
                        <h6>100000</h6>
                    </div>
                    <div class="details-item">
                        <h5>Long market value</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Short market value</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Initial margin</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Maintenance margin</h5>
                        <h6>0</h6>
                    </div>
                    <div class="details-item">
                        <h5>Last maintenance margin</h5>
                        <h6>0</h6>
                    </div>
                </div>
            </div>

            <div class="details-new">
                <a href="{{url('profile')}}" class="btn">Upload New Data</a>
            </div>

            <div class="logout">
                <a class="logout" href="{{url('/logout')}}">LOG OUT</a>
            </div>

        </div>

        <div class="right">

            <div class="top">
                <h3>Your portfolio overview</h3>
                <a href="{{url("/#about")}}" class="btn-outline">About</a>
            </div>

            <div class="result-inputs">
                <div class="trading-bots">
                    <h5 class="mb-2">Do you want to use <span>the trading bot?</span></h5>
                    <input type="radio" id="contactChoice1"
                           name="contact" value="email">
                </div>
                <div class="risk-profile">
                    <label>Risk profile</label>
                    <select>
                        <option value="">Risk Neutral</option>
                        <option value="">Risk Adverse</option>
                        <option value="">Risk Taker</option>
                    </select>
                </div>
            </div>

            <div class="charts">
                <div>
                    <img src="{{asset('img/graph2.jpeg')}}" alt="Logo">
                </div>
                <div>
                    <img src="{{asset('img/graph3.jpeg')}}" alt="Logo">
                </div>
            </div>

            <div class="charts2">
                <img src="{{asset('img/graph1.jpeg')}}" alt="Logo">
            </div>

        </div>
    </section>


</body>

<script src="{{asset('js/app.js')}}"></script>

</html>
