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
    public function screen(Request $request)
    {
        $filePath = $request->file('image')->store(config('app.screening_storage_folder'), 'data');
        $screeningResult = Http::get(config('app.pocovidnet') . '/predict?filename=' . config('app.pocovidnet_storage') . $filePath);

        $file = new File();
        $file->path = $filePath;
        $file->save();

        $screening = new Screening();
        $screening->result = $screeningResult;
        $screening->type_id = 3;
        $screening->file_id = $file->id;
        $screening->save();

        return response()->json($screening);
    }

    /**
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function count(Request $request)
    {
        return response()->json([5]);
    }

    /**
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function countCovid(Request $request)
    {
        return response()->json([2]);
    }
}
