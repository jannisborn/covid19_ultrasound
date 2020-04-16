<?php

namespace Backpack\CRUD\Tests\Unit\CrudPanel;

use Backpack\CRUD\app\Library\CrudPanel\CrudPanel;
use Orchestra\Database\ConsoleServiceProvider;

abstract class BaseDBCrudPanelTest extends BaseCrudPanelTest
{
    /**
     * @var CrudPanel
     */
    protected $crudPanel;

    protected $model;

    /**
     * Setup the test environment.
     *
     * @return void
     */
    protected function setUp(): void
    {
        parent::setUp();

        // call migrations specific to our tests
        $this->loadMigrationsFrom([
            '--database' => 'testing',
            '--path' => realpath(__DIR__.'/../../config/database/migrations'),
        ]);

        $this->artisan('db:seed', ['--class' => 'UsersRolesTableSeeder']);
        $this->artisan('db:seed', ['--class' => 'UsersTableSeeder']);
        $this->artisan('db:seed', ['--class' => 'ArticlesTableSeeder']);
    }

    /**
     * Define environment setup.
     *
     * @param \Illuminate\Foundation\Application $app
     *
     * @return void
     */
    protected function getEnvironmentSetUp($app)
    {
        $app['config']->set('database.default', 'testing');
    }

    /**
     * Get package providers.
     *
     * @param \Illuminate\Foundation\Application $app
     *
     * @return array
     */
    protected function getPackageProviders($app)
    {
        return [
            ConsoleServiceProvider::class,
        ];
    }

    /**
     * Assert that the attributes of a model entry are equal to the expected array of attributes.
     *
     * @param array                               $expected attributes
     * @param \Illuminate\Database\Eloquent\Model $actual   model
     */
    protected function assertEntryEquals($expected, $actual)
    {
        foreach ($expected as $key => $value) {
            if (is_array($value)) {
                $this->assertEquals(count($value), $actual->{$key}->count());
            } else {
                $this->assertEquals($value, $actual->{$key});
            }
        }

        $this->assertNotNull($actual->created_at);
        $this->assertNotNull($actual->updated_at);
    }
}
