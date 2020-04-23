<?php

namespace App\Http\Controllers\Api\Screening;

use App\Screening;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class ScreeningController extends Controller
{
    /**
     * @param Request $request
     * @throws \Illuminate\Validation\ValidationException
     */
    public function __invoke(Request $request)
    {
        $this->validate($request, [
            'email' => 'email|required|unique:users,email',
            'name' => 'required|string|min:4|max:255',
            'password' => 'required|string|min:8|confirmed'
        ]);

        $screening = Screening::create([
            'email' => $request->email,
            'name' => $request->name,
            'password' => bcrypt($request->password),
        ]);

        return (new UserResource())->additional();
    }
}
