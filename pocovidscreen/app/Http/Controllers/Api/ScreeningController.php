<?php

namespace App\Http\Controllers\Api;

use App\File;
use App\Screening;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Http;

class ScreeningController extends Controller
{
    /**
     * @param Request $request
     * @return
     * @throws \Illuminate\Validation\ValidationException
     */
    public function __invoke(Request $request)
    {
        $filePath = $request->file('files')->store(config('app.screening_storage_folder'));
        $screeningResult = Http::get(config('app.pocovidnet') . '/predict?filename=' . config('app.pocovidnet_storage') . $filePath);

        $screening = new Screening();
        $screening->user_id = 1;
        $screening->result = $screeningResult;
        $screening->type_id = 3;
        $screening->save();

        $file = new File();
        $file->path = $filePath;
        $file->fileable()->associate($screening)->save();

        return response()->json($screening);
    }
}
