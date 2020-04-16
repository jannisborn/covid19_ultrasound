<?php

namespace Backpack\CRUD\Tests\Unit\CrudPanel;

use Backpack\CRUD\Tests\Unit\Models\Article;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Support\Facades\DB;

class CrudPanelDeleteTest extends BaseDBCrudPanelTest
{
    public function testDelete()
    {
        $this->markTestIncomplete('Not correctly implemented');

        $this->crudPanel->setModel(Article::class);
        $article = Article::find(1);

        $wasDeleted = $this->crudPanel->delete($article->id);

        // TODO: the delete method should not convert the returned result to a string
        $deletedArticle = Article::find(1);
        $this->assertTrue($wasDeleted);
        $this->assertNull($deletedArticle);
    }

    public function testDeleteUnknown()
    {
        $this->expectException(ModelNotFoundException::class);

        $this->crudPanel->setModel(Article::class);
        $unknownId = DB::getPdo()->lastInsertId() + 1;

        $this->crudPanel->delete($unknownId);
    }
}
