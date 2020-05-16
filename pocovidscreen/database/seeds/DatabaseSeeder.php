<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        DB::table('image_types')->insert(['name' => 'X-Ray']);
        DB::table('image_types')->insert(['name' => 'CT']);
        DB::table('image_types')->insert(['name' => 'POCUS']);

        DB::table('pathologies')->insert(['name' => 'Pneumonia']);
        DB::table('pathologies')->insert(['name' => 'COVID-19']);
        DB::table('pathologies')->insert(['name' => 'Healthy']);
        DB::table('pathologies')->insert(['name' => 'Unknown']);

        DB::table('users')->insert([
            'name' => 'Anonymous',
            'email' => 'anonymous@pocovidscreen.org',
            'password' => 'xbd3fjb48t9bvda003fda'
        ]);
    }
}
