<?php

namespace App\Http\Controllers\Api;

use App\File;
use App\Screening;
use App\Training;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Http;

class TrainingController extends Controller
{
    /**
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function train(Request $request)
    {
        $filePath = $request->file('image')->store(config('app.training_storage_folder'));
        $file = new File();
        $file->path = $filePath;
        $file->save();

        $training = new Training();
        $training->type_id = 3;
        $training->file_id = $file->id;
        $training->pathology_id = $request->input('pathologyId');
        $training->save();

        return response()->json($training);
    }

    /**
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function count(Request $request)
    {
        return response()->json([]);
    }
}
