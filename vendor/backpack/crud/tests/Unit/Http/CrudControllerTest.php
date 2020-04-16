<?php

namespace Backpack\CRUD\Tests\Unit\Http;

use Backpack\CRUD\app\Library\CrudPanel\CrudPanel;
use Backpack\CRUD\Tests\BaseTest;

class CrudControllerTest extends BaseTest
{
    /**
     * Define environment setup.
     *
     * @param  \Illuminate\Foundation\Application  $app
     * @return void
     */
    protected function getEnvironmentSetUp($app)
    {
        parent::getEnvironmentSetUp($app);
        $controller = '\Backpack\CRUD\Tests\Unit\Http\Controllers\UserCrudController';
        $app['router']->get('users/{id}/edit', "$controller@edit");
        $app['router']->put('users/{id}', "$controller@update");
        $app->singleton('crud', function ($app) {
            return new CrudPanel($app);
        });
    }

    public function testCrudRequestUpdatesOnEachRequest()
    {
        $app = $this->app;

        $firstRequest = $app->get('request')->create('/users/1/edit', 'GET');
        $app->handle($firstRequest);

        $this->assertSame($app->get('crud')->request, $firstRequest);

        $secondRequest = $app->get('request')->create('/users/1', 'PUT', ['name' => 'foo']);
        $app->handle($secondRequest);

        $this->assertSame($app->get('crud')->request, $secondRequest);

        $this->assertNotSame($app->get('crud')->request, $firstRequest);
    }
}
