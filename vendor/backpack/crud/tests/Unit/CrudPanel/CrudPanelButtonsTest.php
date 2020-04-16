<?php

namespace Backpack\CRUD\Tests\Unit\CrudPanel;

use Backpack\CRUD\app\Library\CrudPanel\Traits\CrudButton;

class CrudPanelButtonsTest extends BaseCrudPanelTest
{
    private $defaultButtonNames = [];

    private $topViewButton;
    private $lineViewButton;
    private $bottomViewButton;
    private $topModelFunctionButton;

    protected function setUp(): void
    {
        parent::setUp();

        $this->crudPanel->setOperation('list');

        $this->topViewButton = new CrudButton('top', 'topViewButton', 'view', 'crud::buttons.show');
        $this->lineViewButton = new CrudButton('line', 'lineViewButton', 'view', 'crud::buttons.update');
        $this->bottomViewButton = new CrudButton('bottom', 'bottomViewButton', 'view', 'crud::buttons.revisions');

        $this->topModelFunctionButton = new CrudButton('top', 'topModelFunctionButton', 'someModelFunctionName', 'crud::buttons.show');
    }

    public function testDefaultButtons()
    {
        $this->assertEquals(count($this->defaultButtonNames), count($this->crudPanel->buttons()));

        foreach ($this->crudPanel->buttons() as $button) {
            $this->assertTrue(in_array($button->name, $this->defaultButtonNames));
        }
    }

    public function testAddTopButtonTop()
    {
        $expectedButton = $this->topViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->last());
    }

    public function testAddButtonLine()
    {
        $expectedButton = $this->lineViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->first());
    }

    public function testAddButtonBottom()
    {
        $expectedButton = $this->bottomViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->last());
    }

    public function testAddButtonBottomUnknownStackName()
    {
        $this->markTestIncomplete('Not correctly implemented');

        $this->expectException(\Exception::class);

        $expectedButton = $this->topViewButton;

        // TODO: this should throw an error.
        $this->crudPanel->addButton('unknownStackName', $expectedButton->name, $expectedButton->type, $expectedButton->content);
    }

    public function testAddButtonsWithSameName()
    {
        $expectedButton = $this->topViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);
        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);

        $this->assertEquals(count($this->defaultButtonNames) + 1, count($this->crudPanel->buttons()));
    }

    public function testAddButtonsWithSameNameWithoutReplacing()
    {
        $expectedButton = $this->topViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content, false, false);
        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content, false, false);

        $this->assertEquals(count($this->defaultButtonNames) + 2, count($this->crudPanel->buttons()));
    }

    public function testAddButtonBeginning()
    {
        $expectedButton = $this->topViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content, 'beginning');

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->first());
    }

    public function testAddButtonEnd()
    {
        $expectedButton = $this->lineViewButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content, 'end');

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->last());
    }

    public function testAddButtonUnknownPosition()
    {
        $this->markTestIncomplete('Not correctly implemented');

        $this->expectException(\Exception::class);

        $expectedButton = $this->lineViewButton;

        // TODO: this should throw an error.
        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content, 'unknownPosition');
    }

    public function testAddButtonFromModelFunction()
    {
        $expectedButton = $this->topModelFunctionButton;

        $this->crudPanel->addButton($expectedButton->stack, $expectedButton->name, $expectedButton->type, $expectedButton->content);

        $this->assertEquals($expectedButton, $this->crudPanel->buttons()->last());
    }

    public function testAddButtonFromView()
    {
        $expectedButton = $this->topViewButton;
        $viewName = 'someViewName';

        $this->crudPanel->addButtonFromView($expectedButton->stack, $expectedButton->name, $viewName, $expectedButton->content);

        $backpackButtonViewPackage = 'crud::buttons.';
        $actualButton = $this->crudPanel->buttons()->last();

        $this->assertEquals($expectedButton->stack, $actualButton->stack);
        $this->assertEquals($expectedButton->name, $actualButton->name);
        $this->assertEquals($backpackButtonViewPackage.$viewName, $actualButton->content);
        $this->assertEquals($expectedButton->stack, $actualButton->stack);
    }

    public function testRemoveButton()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');
        $this->crudPanel->removeButton('update');

        $this->assertEquals(0, count($this->crudPanel->buttons()));
        $this->assertNull($this->getButtonByName('update'));
    }

    public function testRemoveButtons()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');
        $this->crudPanel->addButton('line', 'show', 'view', 'crud::buttons.show', 'end');
        $this->crudPanel->removeButtons(['show', 'update']);

        $this->assertEquals(0, count($this->crudPanel->buttons()));
        $this->assertNull($this->getButtonByName('show'));
        $this->assertNull($this->getButtonByName('update'));
    }

    public function testRemoveUnknownButtons()
    {
        $buttonNames = [
            'someButtonName',
            'someOtherButtonName',
        ];

        $this->crudPanel->removeButtons($buttonNames);

        $this->assertEquals(count($this->defaultButtonNames), count($this->crudPanel->buttons()));
    }

    public function testRemoveUnknownButton()
    {
        $buttonName = 'someButtonName';

        $this->crudPanel->removeButton($buttonName);

        $this->assertEquals(count($this->defaultButtonNames), count($this->crudPanel->buttons()));
    }

    public function testRemoveAllButtons()
    {
        $this->crudPanel->removeAllButtons();

        $this->assertEmpty($this->crudPanel->buttons());
    }

    public function testRemoveButtonFromStack()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');

        $button = $this->crudPanel->buttons()->first();

        $this->crudPanel->removeButtonFromStack($button->name, $button->stack);

        $this->assertEquals(0, count($this->crudPanel->buttons()));
        $this->assertNull($this->getButtonByName($button->name));
    }

    public function testRemoveUnknownButtonFromStack()
    {
        $this->crudPanel->removeButtonFromStack('someButtonName', 'line');

        $this->assertEquals(count($this->defaultButtonNames), count($this->crudPanel->buttons()));
    }

    public function testRemoveButtonFromUnknownStack()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');
        $this->crudPanel->addButton('line', 'show', 'view', 'crud::buttons.show', 'end');

        $button = $this->crudPanel->buttons()->first();

        $this->crudPanel->removeButtonFromStack($button->name, 'someStackName');

        $this->assertEquals(2, count($this->crudPanel->buttons()));
    }

    public function testRemoveAllButtonsFromStack()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');
        $this->crudPanel->addButton('line', 'show', 'view', 'crud::buttons.show', 'end');

        $this->crudPanel->removeAllButtonsFromStack('line');

        $this->assertEquals(0, count($this->crudPanel->buttons()));
    }

    public function testRemoveAllButtonsFromUnknownStack()
    {
        $this->crudPanel->removeAllButtonsFromStack('someStackName');

        $this->assertEquals(count($this->defaultButtonNames), count($this->crudPanel->buttons()));
    }

    public function testOrderButtons()
    {
        $this->crudPanel->addButton('line', 'update', 'view', 'crud::buttons.update', 'end');
        $this->crudPanel->addButton('line', 'show', 'view', 'crud::buttons.show', 'end');
        $this->crudPanel->addButton('line', 'test', 'view', 'crud::buttons.test', 'end');

        $this->crudPanel->orderButtons('line', ['show', 'test']);

        $this->assertEquals(['show', 'test', 'update'], $this->crudPanel->buttons()->pluck('name')->toArray());
    }

    private function getButtonByName($name)
    {
        return $this->crudPanel->buttons()->first(function ($value) use ($name) {
            return $value->name == $name;
        });
    }
}
