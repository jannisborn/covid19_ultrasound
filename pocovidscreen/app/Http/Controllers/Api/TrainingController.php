<?php

namespace App\Http\Controllers\Api;

use App\File;
use App\Training;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class TrainingController extends Controller
{
    /**
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function train(Request $request)
    {
        $filePath = $request->file('image')->store(config('app.training_storage_folder'), 'data');
        $file = new File();
        $file->path = $filePath;
        $file->save();

        $training = new Training();
        // @todo add the connected user id... Training are done by authenticated users only.
        $training->user_id = 1;
        $training->type_id = 3;
        $training->file_id = $file->id;
        $training->pathology_id = $request->input('label');
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
