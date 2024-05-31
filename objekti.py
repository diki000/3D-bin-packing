import numpy as np
import math


class Bin():
    def __init__(self, capacity):
        self.capacity = capacity # dimensions of the bin presented as 3-tuple
        self.items = []
        self.EMSs = [[np.array((0, 0, 0)), np.array(capacity)]]
        self.W = capacity[0]
        self.D = capacity[1]
        self.H = capacity[2]

    def get_loaded_volume(self):
        loaded_volume= 0
        for item in self.items:
            loaded_volume += np.product(item[1] - item[0])
        return loaded_volume
    
    
    def adding_new_box(self, box, selected_EMS, remaining_boxes):
        box_to_place = np.array(box)
        selected_min = np.array(selected_EMS[0])
        placed_box = [selected_min, selected_min + box_to_place] #place box in bottom left corner of EMS
        self.items.append(placed_box)
        #Step 1: Get smallest dimension and smallest volume of remaining boxes
        #get smallest dimension and smallest volume of remaining boxes
        min_vol = np.inf
        min_dim = np.inf
        for box in remaining_boxes:
            # smallest dimension
            dim = np.min(box)
            if dim < min_dim:
                min_dim = dim
                
            # smallest volume
            vol = np.product(box)
            if vol < min_vol:
                min_vol = vol

        if remaining_boxes == []:
            min_vol = 0
            min_dim = 0

        # Step 2: Generate new EMSs resulting from the intersection of the box
        for EMS in self.EMSs.copy():
            if overlapped(placed_box, EMS):
                # Eliminate overlapped EMS
                for i in range(len(self.EMSs)):
                    if np.all(self.EMSs[i][0] == EMS[0]) and np.all(self.EMSs[i][1] == EMS[1]):
                        self.EMSs.pop(i)
                        break

                # Generate three new EMSs in 3 dimensions
                x1, y1, z1 = EMS[0]
                x2, y2, z2 = EMS[1]
                x4, y4, z4 = placed_box[1]
                new_EMSs = [
                    [np.array((x4, y1, z1)), np.array((x2, y2, z2))],
                    [np.array((x1, y4, z1)), np.array((x2, y2, z2))],
                    [np.array((x1, y1, z4)), np.array((x2, y2, z2))]
                ]

                for new_EMS in new_EMSs:
                    new_box = new_EMS[1] - new_EMS[0]
                    is_valid = True

                    # Step 3: Eliminate new EMSs which are totally inscribed by other EMSs
                    for other_EMS in self.EMSs:
                        if inscribed(new_EMS, other_EMS):
                            is_valid = False

                    # Step 4: Do not add new EMS smaller than the volume of remaining boxes
                    if np.min(new_box) < min_dim:
                        is_valid = False

                    # Step 5: Do not add new EMS having smaller dimension of the smallest dimension of remaining boxes
                    if np.product(new_box) < min_vol:
                        is_valid = False

                    if is_valid:
                        self.EMSs.append(new_EMS)

def orient(box, direction):
    d, w, h = box
    orientations = {
        1: (d, w, h),
        2: (d, h, w),
        3: (w, d, h),
        4: (w, h, d),
        5: (h, d, w),
        6: (h, w, d)
    }
    return orientations[direction]



def DFTRC2(bin, box, existing_EMSs):
    maxDist = -1
    selectedEMS = None
    for EMS in existing_EMSs:
        for direction in range(1, 7): # 6 directions

            d, w, h = orient(box, direction)
            if fitin((d, w, h), EMS):

                x, y, z = EMS[0]
                distance = (bin.D-x-d)**2 + (bin.W-y-w)**2 + (bin.H-z-h)**2

                if distance > maxDist: # find maximal distance from top right corner
                    maxDist = distance
                    selectedEMS = EMS

    return selectedEMS

def fitin(box, EMS):
    for d in range(3):
        if box[d] > (EMS[1][d] - EMS[0][d]):
            return False
    return True

def overlapped(EMS_1, EMS_2):
    if np.all(EMS_1[1] > EMS_2[0]) and np.all(EMS_1[0] < EMS_2[1]):
        return True
    return False

def inscribed(EMS_1, EMS_2):
    if np.all(EMS_2[0] <= EMS_1[0]) and np.all(EMS_1[1] <= EMS_2[1]):
        return True
    return False

def least_loaded_bin(num_opened_bins, Bins):
    # find least load
    leastLoad = np.inf
    for k in range(num_opened_bins):
        load = Bins[k].get_loaded_volume()
        if load < leastLoad:
            leastLoad = load
    
    least_loaded_ratio = leastLoad / np.product(Bins[0].capacity)
    return least_loaded_ratio % 1

def placement_procedure(BPS, VBO, Bins, boxes):

    # pack box in the order of BPS
    items_sorted = [boxes[i] for i in np.argsort(BPS)]
    global num_opened_bins
    global failed
    num_opened_bins = 1
    failed = False
    selected_bin = -1

    for i, box in enumerate(items_sorted):
            
        # selection Bin and EMS to place the box
        for k in range(num_opened_bins):
            
            # select EMS using DFTRC2 heuristic
            EMS = DFTRC2(Bins[k], box, Bins[k].EMSs)

            # select successfully
            if EMS != None:
                selected_bin = k
                selected_EMS = EMS
                break
        else: # if no Bin is selected
            
            num_opened_bins += 1 
            selected_bin = num_opened_bins - 1
            if num_opened_bins > len(Bins):
                failed = True
                return

            # select the first and only EMS from the new Bin
            selected_EMS = Bins[selected_bin].EMSs[0]
    

        # Box orientation selection
        # feasible direction
        BOs = []
        for direction in range(1, 7):
            if fitin(orient(box, direction), selected_EMS):
                BOs.append(direction)
        
        # choose direction based on VBO vector
        BO = BOs[math.ceil(VBO[i]*len(BOs))-1]
            
        # pack the box to the bin & update state information
        Bins[selected_bin].adding_new_box(orient(box, BO), selected_EMS, items_sorted[i+1:])

def fitness_function(Bins):
    if failed:
        return np.inf
    fitness = 0
    fitness += num_opened_bins
    #get least loaded bin
    fitness += least_loaded_bin(num_opened_bins, Bins)
    return fitness

