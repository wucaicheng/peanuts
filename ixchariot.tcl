# return type
# -1 : Define a script for pair failed
# -2 : Add the pair to the test failed
# -3 : Run ixchariot test failed
# -4 : Ixchariot cannot stop when the test timeout
# -5 : Ixchariot running error, no date
# -6 : Save result failed
# -7 : Ixchariot running error, no elapsed time

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
#set NetIQ "c:/Program Files (x86)/Ixia/IxChariot"
#cd $NetIQ

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
# the results from it. We'll wait for durition+30s here, then
# call it an error if it has not yet stopped.
#puts "Wait for the test to stop..."
if {![chrTest isStopped $test $timeout]} { 
  #puts "ERROR: Test didn't stop in $timeout second!"
  chrTest stop $test
  chrTest abandon $test
  set stopCheck 0
  set loop 1
  while {!($stopCheck) && ($loop <10)} {
   set stopCheck [chrTest isStopped $test 2]
   incr loop
   }
  catch {chrTest delete $test force}
  return -4
}
 
# Now let's get some results:
# the throughput (avg, min, max)
#puts ""
#puts "Test results:\n------------"

set SendTotal 0
set RecvTotal 0
set time 0
for {set j 0} {$j < $pairs} {incr j} {
#Total date , Bytes
if {[catch {set SendD [chrCommonResults get $pair BYTES_SENT_E1]}]} {
    return -5
}
set SendTotal [expr $SendTotal + $SendD]
set RecvD [chrCommonResults get $pair BYTES_RECV_E1]
set RecvTotal [expr $RecvTotal + $RecvD]

#elapsed time
if {[catch {set num [expr [chrPair getTimingRecordCount $pair] -1]}]} {
    return -7
}
set timeR [chrPair getTimingRecord $pair $num]
set elapsed [chrTimingRec get $timeR ELAPSED_TIME ]
#puts "time======$eplased"
if {$elapsed > $time} {
set time $elapsed
}
incr pair -1
}
set total [expr ($SendTotal +$RecvTotal) / 125000]
set avg [expr $total / $time]

# Finally, let's save the test so we can look at it again.
if {[catch {chrTest save $test $testFile}]} {
  return -6
}

return [format "%.3f" $avg]
#chrTest delete $test force
}

#puts "=============ixchariot running============="

runtest $ae1 $ae2 $protocol $pairCount $duration $script2 $resultPath
