# return type
# -1 : Define a script for pair failed
# -2 : Add the pair to the test failed
# -3 : Run ixchariot test failed
# -4 : Ixchariot cannot stop when the test timeout
# -5 : Ixchariot finished but no result

#options
list args
set ae1 [lindex $args 0]
set ae2 [lindex $args 1]
set script2 [lindex $args 2]
set protocol [lindex $args 3]
set pairCount [lindex $args 4]
set duration [lindex $args 5]
set resultPath [lindex $args 6]

# Where you installed NetIQ��s Chariot
set NetIQ "c:/Program Files (x86)/Ixia/IxChariot"
cd $NetIQ

#load the Chariot
load ChariotExt
package require ChariotExt
global auto_index

#create thread and run ixchariot
proc runtest {e1 e2 proto pairs duration1 script1 testFile} {
set script "c:/Program Files (x86)/Ixia/IxChariot/Scripts/"
append script $script1
#set testFile "d:/results.tst"
set timeout [expr $duration1 + 30]
set test [chrTest new] 

#config run options 
set runOpts [chrTest getRunOpts $test]
chrRunOpts set $runOpts TEST_END FIXED_DURATION
chrRunOpts set $runOpts TEST_DURATION $duration1

#creat pairs
for {set index 0} {$index < $pairs} {incr index} {

# Create a pair.
set pair [chrPair new]

# Set pair attributes from our lists.
chrPair set $pair COMMENT "Pair [expr $index + 1]"
chrPair set $pair E1_ADDR $e1 E2_ADDR $e2 
chrPair set $pair PROTOCOL $proto
#chrPair useScript $pair $script 
#chrPair useScript  $pair $script

# Define a script for use by this pair.
# We need to check for errors with extended info here.
if {[catch {chrPair useScript $pair $script}]} {
#pLogError $pair $errorCode "chrPair useScript"
   catch {chrTest delete $test}
   return -1
}

# Add the pair to the test.
if {[catch {chrTest addPair $test $pair}]} {
#pLogError $test $errorCode "chrTest addPair"
  catch {chrTest delete $test}
  return -2
}
}

# We have a test defined, so now we can run it.
if {[catch {chrTest start $test}]} {
  return -3
}

# We have to wait for the test to stop before we can look at
# the results from it. We'll wait for 2 minutes here, then
# call it an error if it has not yet stopped.
puts "Wait for the test to stop..." 
if {![chrTest isStopped $test $timeout]} { 
  puts "ERROR: Test didn't stop in $timeout second!"
  chrTest stop $test
  set stopCheck 0
  while {$stopCheck!=1} {
   set stopCheck [chrTest isStopped $test 2]
   }
  catch {chrTest delete $test force}
  return -4
}
 
# Now let's get some results:
# the throughput (avg, min, max)
puts "" 
puts "Test results:\n------------"

set sumavg 0
for {set j 0} {$j < $pairs} {incr j} {
if {[catch {set mtime [chrCommonResults get $pair MEAS_TIME]}]} {
    return -5
}
#set mtime [chrCommonResults get $pair MEAS_TIME]
set throughput [chrPairResults get $pair THROUGHPUT]
set avg [format "%.3f" [lindex $throughput 0]]
set sumavg [expr $sumavg + [expr $avg * $mtime]]
incr pair -1
}
set Fsumavg [expr $sumavg / [format "%.3f" [expr $duration1 - 0.02]]]

# Finally, let's save the test so we can look at it again. 
puts "==========" 
puts "Save the test..." 
catch {chrTest save $test $testFile}
return [format "%.1f" $Fsumavg]
#chrTest delete $test force
}

puts "=============ixchariot running============="

runtest $ae1 $ae2 $protocol $pairCount $duration $script2 $resultPath
