@extends('layouts.app')

@section('content')

    <form class="profile-form" method="POST" action="{{ route('login') }}">

        <div class="profile-header">
            <h2>Welcome!</h2>
            <p class="desc">Give us more details so we can calculate the risk profile algo.</p>
            <p class="message">Upload only CSV files</p>
        </div>

        <div class="profile-form">
            <div class="group-form">
                <label for="">Cash flow</label>
            </div>
            <div class="group-form">
                <label for="">Balance Sheet</label>
            </div>
            <div class="group-form">
                <label for="">Incoming statement</label>
            </div>
            <div class="group-form">
                <label for="">Recent press release, news, articles*</label>
            </div>
        </div>

        <div class="profile-footer">
            <button class="btn">Create Analysis</button>
        </div>

    </form>

@endsection
