<?php

namespace App\Http\Controllers\Admin;

use App\File;
use App\Models\Screening;
use Backpack\CRUD\app\Http\Controllers\CrudController;

/**
 * Class ScreeningCrudController
 * @package App\Http\Controllers\Admin
 * @property-read \Backpack\CRUD\app\Library\CrudPanel\CrudPanel $crud
 */
class ScreeningCrudController extends CrudController
{
    use \Backpack\CRUD\app\Http\Controllers\Operations\ListOperation;

    /**
     * @throws \Exception
     */
    public function setup()
    {
        $this->crud->setModel(Screening::class);
        $this->crud->setRoute(config('backpack.base.route_prefix') . '/screening');
        $this->crud->setEntityNameStrings('Screening', 'Screenings');

        $this->crud->operation('list', function () {
            $this->crud->addColumn([
                'name' => 'created_at',
                'label' => "Creation date",
            ]);
            $this->crud->addColumn([
                'name' => 'file.path',
                'label' => "Image",
                'type' => 'customImage',
                'disk' => 'data',
                'width' => '200px',
                'height' => '200px',
            ]);
            $this->crud->addColumn([
                'name' => 'result',
                'label' => 'Result',
            ]);
        });

        $this->crud->operation('update', function () {
            $this->crud->addField([
                'label' => 'Image',
                'name' => 'file_id',
                'type' => 'customImage',
                'disk' => 'data',
                'crop' => true,
                'aspect_ratio' => 1
            ]);
        });
    }
}
