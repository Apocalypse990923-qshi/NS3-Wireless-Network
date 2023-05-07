#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/txop.h"
#include "ns3/wifi-net-device.h"
#include "ns3/wifi-module.h"
#include <vector>
#include <numeric>

// Default Network Topology
//
//   Wifi 10.1.1.0
//                 AP
//  *    *    *    *
//  |    |    |    |
// n3   n2   n1   n0

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("LAB1");

std::vector<uint32_t> backoff_list;
uint32_t num_txFailed = 0;
uint32_t num_total_tx = 0;

void Calculate_backoff(uint32_t backoff){
  //std::cout << "A new transmission with backoff " << backoff << std::endl;
  backoff_list.push_back(backoff);
}

void Calculate_txfailed(const WifiMacHeader& WifiMacHdr){
  // std::cout << "A transmission failed" << std::endl;
  num_txFailed++;
  num_total_tx++;
}

void Calculate_txok(const WifiMacHeader& WifiMacHdr){
  // std::cout << "A successful transmission" << std::endl;
  num_total_tx++;
}

//void Calculate_txdropped(Ptr<const Packet> pkt){
  // std::cout << "A dropped packet" << std::endl;
  // num_total_tx++;
//}

int 
main (int argc, char *argv[])
{
  // uint32_t N=15; //number of nodes
  double dataRate = 2; // in Mbps
  int noCase = 2;
  uint32_t minCw = 63;
  uint32_t maxCw = 127;
  uint32_t packetSize = 512; // in bytes
  double distance = 10.0; // meters
  double start = 1.0;
  double end = 5.0;
  std::string file_name = "data.csv";

  uint32_t nWifi = 20;
  bool tracing = true;

  CommandLine cmd (__FILE__);
  cmd.AddValue ("nWifi", "Number of wifi STA devices", nWifi);
  cmd.AddValue ("dataRate", "Data rate in Mbps", dataRate);
  cmd.AddValue ("tracing", "Enable pcap tracing", tracing);
  // cmd.AddValue ("minCw", "Minimum content window size", minCw);
  // cmd.AddValue ("maxCw", "Maximum content window size", maxCw);
  cmd.AddValue ("case", "Case A or B for simulation. For case A, input case=1", noCase);
  cmd.AddValue ("file_name","Corresponding file for data saving",file_name);

  cmd.Parse (argc,argv);
  if(noCase == 1){
    minCw = 1;
    maxCw = 1023;
  }
  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (nWifi);
  NodeContainer wifiApNode;
  wifiApNode.Create(1);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  //channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel","Speed", StringValue("1000000"));
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.SetChannel (channel.Create ());

  WifiHelper wifi;
  wifi.SetRemoteStationManager("ns3::IdealWifiManager");


  WifiMacHelper mac;
  Ssid ssid = Ssid ("ns-3-ssid");
  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));

  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, wifiStaNodes);

  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));

  NetDeviceContainer apDevices;
  apDevices = wifi.Install (phy, mac, wifiApNode);

  //backoff window size
  for (uint32_t i = 0; i < nWifi; i++) {
    //Ptr<NetDevice> dev = wifiApNode.Get(0)->GetDevice(0);
    Ptr<WifiNetDevice> wifi_dev = DynamicCast<WifiNetDevice>(wifiStaNodes.Get(i)->GetDevice(0));
    Ptr<WifiMac> wifi_mac = wifi_dev->GetMac();
    PointerValue ptr;
    Ptr<Txop> dca;
    wifi_mac->GetAttribute("Txop", ptr);
    dca = ptr.Get<Txop>();
    dca->SetMinCw(minCw);
    dca->SetMaxCw(maxCw);
    // std::cout << "Node " << i << " MinCw: " << dca->GetMinCw() << std::endl;
    // std::cout << "Node " << i << " MaxCw: " << dca->GetMaxCw() << std::endl;
    dca->TraceConnectWithoutContext("BackoffTrace", MakeCallback(&Calculate_backoff));
    Callback<void, const WifiMacHeader&> txfailed_cb = MakeCallback(&Calculate_txfailed);
    dca->SetTxFailedCallback(txfailed_cb);
    Callback<void, const WifiMacHeader&> txok_cb = MakeCallback(&Calculate_txok);
    dca->SetTxOkCallback(txok_cb);
    //Callback<void, Ptr<const Packet>> txdrop_cb = MakeCallback(&Calculate_txdropped);
    //dca->SetTxDroppedCallback(txdrop_cb);
  }

  //circle
  MobilityHelper mobility;
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator>();
  positionAlloc->Add(Vector(0.0, 0.0, 0.0));
  double r = distance;
  double pi = 3.14159265;
  double theta = 0;
  for(uint32_t i = 0; i <nWifi; i++){
        theta = i*2*pi/nWifi;
        positionAlloc->Add(Vector(r*cos(theta),r*sin(theta),0.0));
  }
  mobility.SetPositionAllocator(positionAlloc);
  mobility.Install(wifiApNode);
  mobility.Install(wifiStaNodes);


  InternetStackHelper stack;
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);

  Ipv4AddressHelper address;

  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer apInterfaces;
  apInterfaces = address.Assign (apDevices);
  Ipv4InterfaceContainer staInterfaces;
  staInterfaces = address.Assign (staDevices);

  uint32_t port = 9;
  ApplicationContainer serverApps;
  for (uint32_t i = 0; i < nWifi; i++) {
    //UdpServerHelper server (port+i);
    PacketSinkHelper sink("ns3::UdpSocketFactory", InetSocketAddress(apInterfaces.GetAddress(0),port+i));
    serverApps.Add(sink .Install(wifiApNode.Get(0)));
  }
  serverApps.Start (Seconds (0.0));
  serverApps.Stop (Seconds (end));

  ApplicationContainer clientApps;
  for (uint32_t i = 0; i < nWifi; i++) {
      OnOffHelper onoff("ns3::UdpSocketFactory",InetSocketAddress(apInterfaces.GetAddress(0),port+i));
      onoff.SetAttribute("PacketSize", UintegerValue(packetSize));
      onoff.SetAttribute("DataRate", DataRateValue(DataRate(dataRate * 1000000)));
      onoff.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
      onoff.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
      clientApps.Add(onoff.Install(wifiStaNodes.Get(i)));
  }
  clientApps.Start (Seconds (start));
  clientApps.Stop (Seconds (end));

  if (tracing == true)
  {
      phy.EnablePcap ("lab1", apDevices.Get (0));
  }

  Simulator::Stop (Seconds (end));
  Simulator::Run ();
  Simulator::Destroy ();

  // Calculate throughput
  
  double duration = end-start;
  //std::cout << "Duration: " << duration << std::endl;
  uint32_t totalRx = 0; //bytes
  std::ofstream node;
  node.open("pernode.csv", std::ofstream::app);
  for (uint32_t i = 0; i < nWifi; i++) {
    Ptr<PacketSink> sink = DynamicCast<PacketSink>(serverApps.Get(i));
    uint32_t rxBytes = sink->GetTotalRx();
    totalRx += rxBytes;
    double throughput = (rxBytes * 8) / duration / 1000000.0; // in Mbps
    std::cout << "Node " << i << " Throughput: " << throughput << " Mbps" << std::endl;
  }
  node.close();
  std::ofstream file;
  file.open(file_name, std::ofstream::app);
  double totalThroughput = (totalRx * 8) / duration / 1000000.0; // in Mbps
  double avgThroughput = totalThroughput/nWifi;
  double avgBackoff = std::accumulate(backoff_list.begin(), backoff_list.end(), 0)*1.0/backoff_list.size();
  double var = 0.0;
  for(uint32_t backoff : backoff_list){
    var += pow(((double)(backoff - avgBackoff)),2);
  }
  var = var * 1.0 / backoff_list.size();
  double collision_rate = num_txFailed*1.0/num_total_tx;
  std::cout << "Average throughput: " << avgThroughput << " Mbps " << std::endl;
  file << totalThroughput <<","<<avgThroughput<<","<<avgBackoff <<","<< collision_rate <<","<< var << std::endl;
  file.close();
  std::cout << "Total throughput: " << totalThroughput << " Mbps " << std::endl;
  std::cout << "Average throughput: " << avgThroughput*1.0 << " Mbps " << std::endl;
  std::cout << "Average backoff time slots per transmission: " << avgBackoff << std::endl;
  std::cout << "Variance of backoff time slots per transmission: " << backoff_var << std::endl;
  std::cout << "Collision rate(failing attempts of transmission): " << collision_rate << std::endl;
  std::cout << "Varince of backoff tiem slots is "<< var << std::endl;
  return 0;
}