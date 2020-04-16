<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class UsersRolesTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('roles')->insert([
            [
                'id'   => 1,
                'name' => 'admin',
            ], [
                'id'   => 2,
                'name' => 'user',
            ],
        ]);
    }
}
