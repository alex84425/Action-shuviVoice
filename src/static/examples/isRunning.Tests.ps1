Describe "Test-MyScript" {
    BeforeAll {
        # Set up any necessary test data or mocks here
    }

    AfterAll {
        # Clean up any test data or mocks here
    }

    Context "When status.txt not exists" {
        BeforeEach {
            Mock Test-Path { return $false }
        }

        It "can not found status.txt after onstart, should return RETRY" {
            $ErrorActionPreference = "Stop"
            & $PSCommandPath.Replace('.Tests', '')
            $LASTEXITCODE | Should -BeExactly 0
        }
    }
    Context "When status.txt exists" {
        BeforeEach {
            Mock Test-Path { return $true }
        }
        
        It "status.txt is FAIL, should exit < 0" {
            $ErrorActionPreference = "Stop"
            Mock Get-Content { return "FAIL" }
            & $PSCommandPath.Replace('.Tests', '')
            $LASTEXITCODE | Should -BeLessThan 0
        }
        It "status.txt is PASS, should exit > 0" {
            $ErrorActionPreference = "Stop"
            Mock Get-Content { return "PASS" }
            & $PSCommandPath.Replace('.Tests', '')
            $LASTEXITCODE | Should -BeGreaterThan 0
        }
    }
}
