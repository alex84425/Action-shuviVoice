BeforeAll {

}


Describe "Test-MyScript" {
    BeforeAll {
        # Set up any necessary test data or mocks here
    }

    AfterAll {
        # Clean up any test data or mocks here
    }

    Context "When status.txt exists and contains PASS" {
        BeforeEach {
            # Set up test conditions for this context here                                    
            Mock Test-Path { return $true }
            Mock Get-Content { return "PASS" }
        }

        AfterEach {
            # Clean up test conditions for this context here            

        }

        It "process not exist mean finish, should exit with code 1" {
            $ErrorActionPreference = "Stop"                        
            
            & $PSCommandPath.Replace('.Tests', '') 
            $exitCode = $LASTEXITCODE
            $exitCode | Should -Be 1
            
        }

        It "process exist, should exit with code 0" {            
            $ErrorActionPreference = "Stop"                        
            Mock Get-Process { return @{ Name = "notepad" } }
            & $PSCommandPath.Replace('.Tests', '') 
            $exitCode = $LASTEXITCODE
            $exitCode | Should -Be 0
            
        }
    }

    Context "When status.txt not exists" {
        BeforeEach {
            # Set up test conditions for this context here
                        
        }

        AfterEach {
            # Clean up test conditions for this context here                        
        }
            
        It "can not found status.txt after onstart, should exit with code 1" {
            $ErrorActionPreference = "Stop"                        
            
            & $PSCommandPath.Replace('.Tests', '') 
            $exitCode = $LASTEXITCODE
            $exitCode | Should -Be 1
            
        }

    }    
    Context "When status.txt is Fail" {
        BeforeEach {
            # Set up test conditions for this context here
            Mock Test-Path { return $true }
            Mock Get-Content { return "FAIL" }
        }

        AfterEach {
            # Clean up test conditions for this context here            
            
        }

        It "status.txt is FAIL, should exit 1" {
            $ErrorActionPreference = "Stop"                        
            
            & $PSCommandPath.Replace('.Tests', '') 
            $exitCode = $LASTEXITCODE
            $exitCode | Should -Be 1
            
        }

   

    }        
}