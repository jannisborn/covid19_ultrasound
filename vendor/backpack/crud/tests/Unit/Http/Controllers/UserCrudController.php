<?php

namespace Backpack\CRUD\Tests\Unit\Http\Controllers;

use Backpack\CRUD\app\Http\Controllers\CrudController;
use Illuminate\Support\Facades\Response;

class UserCrudController extends CrudController
{
    public function setup()
    {
        $this->crud->setModel(User::class);
        $this->crud->setRoute('users');
    }

    protected function edit($id)
    {
        return Response('edit');
    }

    protected function update($id)
    {
        return Response('update');
    }
}
