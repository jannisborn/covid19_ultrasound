<?php

namespace Backpack\CRUD\app\Exceptions;

use Exception;

class AccessDeniedException extends Exception
{
    /**
     * Render the exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request
     *
     * @return \Illuminate\Http\Response
     */
    public function render($request)
    {
        return response(view('errors.403', ['exception' => $this]), 403);
    }
}
