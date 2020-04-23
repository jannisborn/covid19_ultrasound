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
    }
}
