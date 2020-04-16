<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\Schema;

class CreateColumnTypesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        // uncomment the next statement to map strings to enum types in doctrine and get over the 'Unknown database type enum' DBAL error
        // Schema::getConnection()->getDoctrineSchemaManager()->getDatabasePlatform()->registerDoctrineTypeMapping('enum', 'string');

        Schema::create('column_types', function ($table) {
            $table->bigInteger('bigIntegerCol');
            $table->binary('binaryCol');
            $table->boolean('booleanCol');
            $table->char('charCol', 4);
            $table->date('dateCol');
            $table->dateTime('dateTimeCol');
            $table->dateTimeTz('dateTimeTzCol');
            $table->decimal('decimalCol', 5, 2);
            $table->double('doubleCol', 15, 8);
            $table->enum('enumCol', ['foo', 'bar']);
            $table->float('floatCol');
            $table->integer('integerCol');
            $table->ipAddress('ipAddressCol');
            $table->json('jsonCol');
            $table->jsonb('jsonbCol');
            $table->longText('longTextCol');
            $table->macAddress('macAddressCol');
            $table->mediumInteger('mediumIntegerCol');
            $table->mediumText('mediumTextCol');
            $table->smallInteger('smallIntegerCol');
            $table->string('stringCol');
            $table->text('textCol');
            $table->time('timeCol');
            $table->timeTz('timeTzCol');
            $table->tinyInteger('tinyIntegerCol');
            $table->timestamp('timestampCol');
            $table->timestampTz('timestampTzCol')->nullable();
            $table->uuid('uuidCol');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('column_types');
    }
}
