<?php

namespace Backpack\CRUD;

trait LicenseCheck
{
    /**
     * Check to to see if a license code exists.
     * If it does not, throw a notification bubble.
     *
     * @return void
     */
    private function checkLicenseCodeExists()
    {
        // don't even check if it's a console command or unit tests
        if ($this->app->runningInConsole() || $this->app->runningUnitTests()) 
        {
            return;
        }

        // don't show notice bubble on localhost
        if (in_array($_SERVER['REMOTE_ADDR'] ?? [], ['127.0.0.1', '::1'])) {
            return;
        }

        // don't show notice bubble if debug is true
        if (config('app.debug') == 'true' && config('app.env') == 'local') {
            return;
        }

        if (! $this->validCode(config('backpack.base.license_code'))) {
            \Alert::add('warning', "<strong>You're using unlicensed software.</strong> Please ask your web developer to <a target='_blank' class='alert-link text-white' href='http://backpackforlaravel.com'>purchase a license code</a> to hide this message.");
        }
    }

    /**
     * Check that the license code is valid for the version of software being run.
     * 
     * This method is intentionally obfuscated. It's not terribly difficult to crack, but consider how 
     * much time it will take you to do so. It might be cheaper to just buy a license code. 
     * And in the process, you'd support the people who have created it, and who keep putting in time, 
     * every day, to make it better.
     * 
     * @param  string $j License Code
     * @return Boolean
     */
    private function validCode($j)
    {
        $k = str_replace('-', '', $j); $s = substr($k, 0, 8); $c = substr($k, 8, 2); $a = substr($k, 10, 2); $l = substr($k, 12, 2); $p = substr($k, 14, 2); $n = substr($k, 16, 2); $m = substr($k, 18, 2); $z = substr($k, 20, 24); $w = 'ADEFHKLMVWXYZ146'; $x = $s; for ($i = 0; $i < strlen($w); $i++) { $r = $w[$i]; $x = str_replace($r, '-', $x); } $x = str_replace('-', '', $x); if ($x != '') { return false; } if (substr_count($j, '-') != 5) { return false; } $e = substr(crc32(substr($k, 0, 20)), -4); if ($z !== $e) { return false; } $o = strrev(substr(preg_replace('/[0-9]+/', '', strtoupper(sha1($a.'sand('.$s.')'.$n.'tos()'))), 2, 2)); if ($m !== $o) { return false; } return true;
    }
}
