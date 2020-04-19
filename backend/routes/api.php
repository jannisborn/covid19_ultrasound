<?php

use App\Models\TeamMember;
use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::get('/team-members', function (Request $request) {
    TeamMember::create(['full_name' => 'Toto']);
    return TeamMember::get(['*']);
});
