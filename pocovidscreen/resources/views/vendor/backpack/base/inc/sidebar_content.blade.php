<!-- This file is used to store sidebar items, starting with Backpack\Base 0.9.0 -->
<li class="nav-item"><a class="nav-link" href="{{ backpack_url('dashboard') }}"><i class="fa fa-dashboard nav-icon"></i> {{ trans('backpack::base.dashboard') }}</a></li>
<li class="nav-item"><a class="nav-link" href="{{ backpack_url('elfinder') }}\"><i class="nav-icon fa fa-files-o"></i> <span>{{ trans('backpack::crud.file_manager') }}</span></a></li>
<li class="nav-item nav-dropdown">
    <a class="nav-link nav-dropdown-toggle" href="#data"><i class="fa fa-key"></i> <span>Data</span></a>
    <ul class="nav-dropdown-items" id="data">
        <li class='nav-item'><a class='nav-link' href='{{ backpack_url('training') }}'><i class='nav-icon fa fa-bar-chart'></i> Trainings</a></li>
        <li class='nav-item'><a class='nav-link' href='{{ backpack_url('screening') }}'><i class='nav-icon fa fa-medkit'></i> Screenings</a></li>
    </ul>
</li>
