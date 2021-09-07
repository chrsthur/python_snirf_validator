clear all force
close all hidden
clc
validator();

function validator()
    for Required = 1
    RequiredFields = ["/formatVersion",...
                     "/nirs/metaDataTags/SubjectID",...
                     "/nirs/metaDataTags/MeasurementDate",...
                     "/nirs/metaDataTags/MeasurementTime",...
                     "/nirs/metaDataTags/LengthUnit",...
                     "/nirs/metaDataTags/TimeUnit",...
                     "/nirs/metaDataTags/FrequencyUnit",...
                     "/nirs/data/dataTimeSeries",...
                     "/nirs/data/time",...
                     "/nirs/data/measurementList/sourceIndex",...
                     "/nirs/data/measurementList/detectorIndex",...
                     "/nirs/data/measurementList/wavelengthIndex",...
                     "/nirs/data/measurementList/dataType",...
                     "/nirs/data/measurementList/dataTypeIndex",...
                     "/nirs/probe/wavelengths",...
                     "/nirs/probe/sourcePos2D",...
                     "/nirs/probe/detectorPos2D",...
                     "/nirs/stim/name",...
                     "/nirs/stim/data",...
                     "/nirs/aux/name",...
                     "/nirs/aux/dataTimeSeries",...
                     "/nirs/aux/time"]';
    end
    for Optional = 1
    OptionalFields = ["/nirs/data/measurementList/wavelengthActual",...
                     "/nirs/data/measurementList/wavelengthEmissionActual",...
                     "/nirs/data/measurementList/dataTypeLabel",...
                     "/nirs/data/measurementList/sourcePower",...
                     "/nirs/data/measurementList/detectorGain",...
                     "/nirs/data/measurementList/moduleIndex",...
                     "/nirs/data/measurementList/sourceModuleIndex",...
                     "/nirs/data/measurementList/detectorModuleIndex",...
                     "/nirs/probe/wavelengthsEmission",...
                     "/nirs/probe/sourcePos3D",...
                     "/nirs/probe/detectorPos3D",...
                     "/nirs/probe/frequencies",...
                     "/nirs/probe/timeDelays",...
                     "/nirs/probe/timeDelayWidths",...
                     "/nirs/probe/momentOrders",...
                     "/nirs/probe/correlationTimeDelays",...
                     "/nirs/probe/correlationTimeDelayWidths",...
                     "/nirs/probe/sourceLabels",...
                     "/nirs/probe/detectorLabels",...
                     "/nirs/probe/landmarkPos2D",...
                     "/nirs/probe/landmarkPos3D",...
                     "/nirs/probe/landmarkLabels",...
                     "/nirs/probe/useLocalIndex",...
                     "/nirs/aux/timeOffset",...
                     "/nirs/stim/dataLabels"]';
    end 
    
    [Files,Path] = uigetfile('*.snirf','Select the Components for regression','MultiSelect', 'on');
    if iscell(Files) % if multiple file is selected
        for i = 1:length(Files)
            InvalidList = {};
            FileLocation = [Path char(Files(1,i))];
            OneSnirf = h5info(FileLocation);
            CheckGroup(OneSnirf,FileLocation)
            CheckValid(char(Files(1,i)));
        end
    else % if only one file is selected
        InvalidList = {};
        FileLocation = [Path char(Files)];
        OneSnirf = h5info(FileLocation);
        CheckGroup(OneSnirf,FileLocation);
        CheckValid(char(Files));
    end

    function CheckGroup(Group,FileLocation)
        if isempty(Group.Groups) % no more groups, check sub-dataset
            for j = 1:length(Group.Datasets)
                FieldName = [Group.Name '/' Group.Datasets(j,1).Name];
                fprintf(FieldName);
                CheckField(Group.Datasets(j,1),FieldName,FileLocation);
                fprintf('\n')
            end
        else % still have groups
            if ~isempty(Group.Datasets) % check dataset of group
                for k = 1:length(Group.Datasets)
                    FieldName = [Group.Name '/' Group.Datasets(k,1).Name];
                    fprintf(FieldName)
                    CheckField(Group.Datasets(k,1),FieldName,FileLocation);
                    fprintf('\n')
                end
            end
            for a = 1:length(Group.Groups)
                CheckGroup(Group.Groups(a,1),FileLocation)
            end 
        end
    end

    function CheckField(DataSet,FieldName,FileLocation)
        FieldNameFcn = FieldName;
        Data = h5read(FileLocation,FieldName);
        if ~contains(FieldName,'probe')
            FieldNameFcn = regexp(FieldName,'[\D]','match');
            FieldNameFcn = strjoin(FieldNameFcn,'');
        end
        
        % Required/Optional Check
        if contains(FieldNameFcn,RequiredFields)
            if contains(FieldNameFcn,'aux') || contains(FieldNameFcn,'stim')
                fprintf('    Required field when optional parent group is included!');
                CheckDim(Data,DataSet,FieldName,0);
            else
                fprintf('    Required Field!');
                CheckDim(Data,DataSet,FieldName,0);
            end
        elseif contains(FieldNameFcn,OptionalFields)
            fprintf('    Optional Field!');
            CheckDim(Data,DataSet,FieldName,0);
        else 
            if contains(FieldNameFcn,'/nirs/metaDataTags/')
               fprintf('    User Customized Field!');
               CheckDim(Data,DataSet,FieldName,1);
            else
               fprintf('    Invalid Fields!');
               InvalidList{end+1,1} = FieldName;
            end
        end
    end

    function CheckDim(Data,DataSet,FieldName,Customize)
        % Dimension Check
        ActualDim = GetActualDim(DataSet,Data);
        SpecDim = GetSpecDim(FieldName);
        fprintf('\n');
        % ignore user customized field
        if Customize == 1
            SpecDim = ActualDim;
        end
        
        % Dimension adjustment for /nirs/stim/data, 
        if contains(FieldName,'stim') && contains(FieldName,'data')
            if ~contains(FieldName,'dataLabels')
                if max(size(Data,1),size(Data,2)) >= 3
                    ActualDim = 2;
                end
            end
        end
          
        if ~isequal(SpecDim,ActualDim) 
            fprintf('    Invalid dimenswions! Expected Number of dimension: %d',SpecDim);
            fprintf('\n');
            InvalidList{end+1,1} = FieldName;
        end
    end

    function ActualDim = GetActualDim(DataSet,Data)
        [row,col] = size(Data);
        %ActualDim = [];
        ActualDim = 1;
        fprintf('\n');
        % Get actual dimension 
        if isstring(Data) || iscell(Data) % string
           str = sprintf('%dx%d string, ',row,col);
           fprintf('    Data type: %s %s',DataSet.Datatype.Class,str);
           fprintf('%s ',Data{:})
            %ActualDim = 1;
        elseif isscalar(Data) && isa(Data,'integer') % single integer
           fprintf('    Data type: %s, ',DataSet.Datatype.Class);
           fprintf('%dx%d Integer, %s',row,col,"0D in python, ");
           fprintf('Value: %d',Data);
            %ActualDim = 0;
        elseif isscalar(Data) && isa(Data,'float') % single float
           fprintf('    Data type: %s, ',DataSet.Datatype.Class);
           fprintf('%dx%d Float, %s',row,col,"0D in python, "); 
           fprintf('Value: %.1f',Data);
            %ActualDim = 0;
        elseif isvector(Data)
           fprintf('    Data type: %s, ',DataSet.Datatype.Class);
           fprintf('%dx%d 1D-Vector',row,col);  
            %ActualDim = 1;
        elseif ismatrix(Data)
           fprintf('    Data type: %s, ',DataSet.Datatype.Class);
           fprintf('%dx%d 2D-Vector',row,col);
           ActualDim = 2;
        end
    end

    function SpecDim = GetSpecDim(FieldName)
        if contains(FieldName,'Pos2D') || contains(FieldName,'Pos3D')
            SpecDim = 2;
        elseif contains(FieldName,'dataTimeSeries')
            if contains(FieldName,'aux')
                SpecDim = 1;
            else
                SpecDim = 2;
            end
        elseif contains(FieldName,'stim') && contains(FieldName,'data')
            if contains(FieldName,'dataLabels')
                SpecDim = 1;
            else
                SpecDim = 2;
            end
%         elseif contains(FieldName,'measurementList')
%             if contains(FieldName,'dataTypeLabel')
%                 SpecDim = 1;
%             else
%                 SpecDim = 0;
%             end
%         elseif contains(FieldName,'useLocalIndex')
%             SpecDim = 0;
        else
           SpecDim = 1; 
        end    
    end

    function CheckValid(OneFile)
        fprintf('%c','----------------------');
        fprintf('\n');
        if isempty(InvalidList)
            fprintf('%s is valid!',OneFile);
        else
            fprintf('%s is not valid!\n',OneFile);
            for z = 1:length(InvalidList)
               fprintf('%s\n',char(InvalidList{z,1}));
            end
        end
        fprintf('\n');
    end
end