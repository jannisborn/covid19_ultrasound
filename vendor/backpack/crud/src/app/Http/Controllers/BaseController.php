<?php

namespace Backpack\CRUD\app\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Bus\DispatchesJobs;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller;

/**
 * @deprecated This file is no longer needed, since it's identical with Illuminate\Routing\Controller
 *
 * If you've imported or extended our BaseController
 * (Backpack/Base/app/Http/Controllers/BaseController or Backpack/CRUD/app/Http/Controllers/BaseController)
 * anywhere inside your app, you should use Illuminate\Routing\Controller instead.
 *
 * We haven't removed this class in this version, but it will be removed in the next major version.
 */
class BaseController extends Controller
{
    use AuthorizesRequests, DispatchesJobs, ValidatesRequests;
}
